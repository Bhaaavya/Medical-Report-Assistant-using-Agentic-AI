from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import (
    User,
    Report,
    ReportText,
    ClinicalFinding,
    ExtractedFinding,
    Conversation
)
from app.schemas import ChatRequest, ChatResponse, ChatHistoryResponse
from app.services.llm_router import llm_router
from app.agents.qa_graph import qa_graph
from langsmith import traceable


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/{report_id}/ask", response_model=ChatResponse)
@traceable(name="Medical Report Q&A")
def ask_report_question(
    report_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.user_id == current_user.id
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report_text = (
        db.query(ReportText)
        .filter(ReportText.report_id == report_id)
        .first()
    )

    if not report_text:
        raise HTTPException(status_code=404, detail="Extracted report text not found")

    clinical_findings = (
        db.query(ClinicalFinding)
        .filter(ClinicalFinding.report_id == report_id)
        .all()
    )

    lab_findings = (
        db.query(ExtractedFinding)
        .filter(ExtractedFinding.report_id == report_id)
        .all()
    )

    clinical_context = "\n".join(
        [f"- {item.finding_text}" for item in clinical_findings]
    )

    lab_context = "\n".join(
        [f"- {item.test_name}: {item.value} {item.unit or ''}" for item in lab_findings]
    )

    # --- NEW LANGGRAPH QA GRAPH REPLACEMENT ---
    result = qa_graph.invoke(
        {
            "report_id": report.id,
            "report_type": report.report_type,
            "report_text": report_text.raw_text,
            "language": request.language.value,
            "question": request.question
        }
    )

    answer = result["answer"]
    # ------------------------------------------

    conversation = Conversation(
        user_id=current_user.id,
        report_id=report.id,
        question=request.question,
        answer=answer,
        language=request.language.value
    )

    db.add(conversation)
    db.commit()

    return {
        "report_id": report.id,
        "question": request.question,
        "answer": answer,
        "language": request.language
    }


@router.get("/{report_id}/history", response_model=List[ChatHistoryResponse])
def get_chat_history(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.user_id == current_user.id
        )
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.report_id == report_id,
            Conversation.user_id == current_user.id
        )
        .order_by(Conversation.created_at.asc())
        .all()
    )

    return conversations