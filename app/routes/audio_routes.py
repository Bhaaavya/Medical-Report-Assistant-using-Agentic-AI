from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user

from app.models import (
    User,
    Report,
    ReportText,
    AgentOutput,
    AudioFile
)

from app.schemas import (
    AudioRequest,
    AudioResponse
)

from app.agents.audio_graph import audio_graph
from langsmith import traceable


router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)


@router.post(
    "/{report_id}/generate",
    response_model=AudioResponse
)
@traceable(name="Generate Audio Narration")
def generate_audio(
    report_id: int,
    request: AudioRequest,
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

    result = audio_graph.invoke(
        {
            "report_id": report.id,
            "report_type": report.report_type,
            "report_text": report_text.raw_text,
            "language": request.language.value
        }
    )

    audio_path = result["audio_path"]

    audio_file = AudioFile(
        report_id=report.id,
        language=request.language.value,
        audio_path=audio_path,
        source_output_type=request.output_type
    )

    db.add(audio_file)

    output = AgentOutput(
        report_id=report.id,
        output_type="audio_generation",
        content=audio_path,
        language=request.language.value,
        model_used="gTTS"
    )

    db.add(output)
    db.commit()

    return {
        "report_id": report.id,
        "language": request.language.value,
        "audio_path": audio_path
    }