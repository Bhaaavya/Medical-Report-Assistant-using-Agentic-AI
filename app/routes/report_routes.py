import os
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Report, ReportText, ExtractedFinding, ClinicalFinding, User
from app.schemas import ReportResponse
from app.auth import get_current_user
from app.services.pdf_service import extract_report_content
from typing import List
from app.models import ReportText
from app.schemas import ReportTextDetailResponse

from app.services.report_classifier import detect_report_type
from app.models import ExtractedFinding
from app.services.finding_extractor import extract_findings_from_text
from app.models import ClinicalFinding
from app.services.clinical_finding_extractor import extract_clinical_findings
from typing import List
from app.schemas import ClinicalFindingResponse


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)


@router.post("/upload", response_model=ReportResponse)
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = f"{UPLOAD_DIR}/{current_user.id}_{file.filename}"

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    report = Report(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        file_size=len(contents)
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    extracted = extract_report_content(file_path)
    report_type = detect_report_type(extracted["raw_text"])

    report.report_type = report_type
    db.commit()
    db.refresh(report)

    print("EXTRACTION METHOD:", extracted["extraction_method"])
    print("TEXT LENGTH:", len(extracted["raw_text"]))
    print("QUALITY:", extracted["extraction_quality"])

    report_text = ReportText(
        report_id=report.id,
        raw_text=extracted["raw_text"],
        extraction_method=extracted["extraction_method"],
        extraction_quality=extracted["extraction_quality"],
        page_count=extracted["page_count"],
        needs_ocr=extracted["needs_ocr"]
    )

    db.add(report_text)
    db.commit()

    findings = extract_findings_from_text(extracted["raw_text"])
    print("FINDINGS FOUND:", findings)
    print("TOTAL FINDINGS:", len(findings))
    for item in findings:
        finding = ExtractedFinding(
            report_id=report.id,
            test_name=item["test_name"],
            value=item["value"],
            unit=item["unit"],
            reference_range=item["reference_range"],
            source_text=item["source_text"]
        )
        db.add(finding)
    db.commit()

    clinical_findings = extract_clinical_findings(extracted["raw_text"])
    for item in clinical_findings:
        clinical_finding = ClinicalFinding(
            report_id=report.id,
            finding_text=item["finding_text"],
            body_area=item["body_area"],
            severity=item["severity"],
            source_section=item["source_section"]
        )
        db.add(clinical_finding)
    db.commit()

    return report


@router.get("/list", response_model=List[ReportResponse])
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reports = (
        db.query(Report)
        .filter(Report.user_id == current_user.id)
        .all()
    )

    return reports

@router.get(
    "/{report_id}/text",
    response_model=ReportTextDetailResponse
)
def get_report_text(
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

    return report_text

@router.get(
    "/{report_id}/clinical-findings",
    response_model=List[ClinicalFindingResponse]
)
def get_clinical_findings(
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
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    findings = (
        db.query(ClinicalFinding)
        .filter(ClinicalFinding.report_id == report_id)
        .all()
    )

    return findings

@router.delete("/{report_id}")
def delete_report(
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
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    db.query(ReportText).filter(ReportText.report_id == report_id).delete()
    db.query(ExtractedFinding).filter(ExtractedFinding.report_id == report_id).delete()
    db.query(ClinicalFinding).filter(ClinicalFinding.report_id == report_id).delete()

    if report.file_path and os.path.exists(report.file_path):
        os.remove(report.file_path)

    db.delete(report)
    db.commit()

    return {"message": "Report deleted successfully"}
