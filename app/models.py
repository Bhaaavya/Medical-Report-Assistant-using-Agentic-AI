from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("Report", back_populates="owner")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    report_type = Column(String, default="General Medical Report")
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    audio_files = relationship("AudioFile")

    owner = relationship("User", back_populates="reports")

    extracted_text = relationship(
        "ReportText",
        back_populates="report",
        uselist=False
    )

    findings = relationship(
        "ExtractedFinding",
        back_populates="report"
    )
    
    clinical_findings = relationship(
        "ClinicalFinding",
        back_populates="report"
    )

    agent_outputs = relationship(
        "AgentOutput",
        back_populates="report"
    )

class ReportText(Base):
    __tablename__ = "report_texts"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)

    raw_text = Column(Text, nullable=False)
    extraction_method = Column(String, nullable=False)
    extraction_quality = Column(String, nullable=False)
    page_count = Column(Integer)
    needs_ocr = Column(Boolean, default=False)

    report = relationship("Report", back_populates="extracted_text")

class ExtractedFinding(Base):
    __tablename__ = "extracted_findings"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)

    test_name = Column(String, nullable=False)
    value = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    reference_range = Column(String, nullable=True)

    source_text = Column(Text, nullable=True)

    report = relationship("Report", back_populates="findings")


class ClinicalFinding(Base):
    __tablename__ = "clinical_findings"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=False
    )

    finding_text = Column(Text, nullable=False)

    body_area = Column(String)

    severity = Column(String)

    source_section = Column(String)

    report = relationship(
        "Report",
        back_populates="clinical_findings"
    )

class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)

    output_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String, default="English")
    model_used = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    report = relationship("Report", back_populates="agent_outputs")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    language = Column(String, default="English")

    created_at = Column(DateTime, default=datetime.utcnow)


class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)

    language = Column(String, default="English")
    audio_path = Column(String, nullable=False)
    source_output_type = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)