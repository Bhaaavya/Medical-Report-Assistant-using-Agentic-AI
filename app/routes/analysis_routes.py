from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import User, Report, ReportText, ClinicalFinding, ExtractedFinding, AgentOutput
from app.schemas import SummaryResponse
from app.services.llm_router import llm_router
from app.config import GEMINI_MODEL
from app.schemas import (
    SummaryResponse,
    ExplanationRequest,
    ExplanationResponse
)
from app.agents.graph import medical_graph
from langsmith import traceable

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.post("/{report_id}/summary", response_model=SummaryResponse)
def generate_summary(
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

    report_text = (
        db.query(ReportText)
        .filter(ReportText.report_id == report_id)
        .first()
    )

    if not report_text:
        raise HTTPException(status_code=404, detail="Extracted text not found")

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

    findings_text = "\n".join(
        [f"- {item.finding_text}" for item in clinical_findings]
    )

    lab_text = "\n".join(
        [f"- {item.test_name}: {item.value} {item.unit or ''}" for item in lab_findings]
    )

    prompt = f"""
You are a medical report assistant.

Create a safe, patient-friendly summary of this medical report.

Report Type: {report.report_type}

Clinical Findings:
{findings_text}

Lab Findings:
{lab_text}

Extracted Report Text:
{report_text.raw_text[:5000]}

Rules:
- Do not diagnose the patient.
- Do not prescribe treatment.
- Explain in simple language.
- Mention that the user should consult a qualified doctor.
- If the report is for an animal/veterinary case, say veterinary doctor instead of human doctor.

Output format:
1. Executive Summary
2. Key Findings
3. Patient-Friendly Explanation
4. Questions to Ask the Doctor
5. Safety Disclaimer
"""

    summary = llm_router.generate(prompt)

    output = AgentOutput(
        report_id=report.id,
        output_type="summary",
        content=summary,
        language="English",
        model_used=GEMINI_MODEL
    )

    db.add(output)
    db.commit()

    return {
        "report_id": report.id,
        "output_type": "summary",
        "content": summary,
        "language": "English"
    }

@router.post(
    "/{report_id}/explain",
    response_model=ExplanationResponse
)
@traceable(name="Generate Patient Explanation")

def generate_patient_explanation(
    report_id: int,
    request: ExplanationRequest,
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
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    report_text = (
        db.query(ReportText)
        .filter(ReportText.report_id == report_id)
        .first()
    )

    if not report_text:
        raise HTTPException(
            status_code=404,
            detail="Extracted text not found"
        )

    # --- NEW LANGGRAPH AGENT RUN REPLACEMENT HERE ---
    result = medical_graph.invoke(
        {
            "report_id": report.id,
            "report_type": report.report_type,
            "report_text": report_text.raw_text,
            "language": request.language.value
        }
    )

    explanation = result["translated_output"]
    # -----------------------------------------------

    output = AgentOutput(
        report_id=report.id,
        output_type="patient_explanation",
        content=explanation,
        language=request.language.value, # Added .value here to keep data clean
        model_used=GEMINI_MODEL
    )

    db.add(output)
    db.commit()

    return {
        "report_id": report.id,
        "language": request.language,
        "content": explanation
    }