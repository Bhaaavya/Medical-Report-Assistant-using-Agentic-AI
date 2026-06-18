from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ReportResponse(BaseModel):
    id: int
    filename: str
    file_size: int
    report_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class ReportTextResponse(BaseModel):
    report_id: int
    raw_text: str
    extraction_method: str
    extraction_quality: str
    page_count: int | None
    needs_ocr: bool

    class Config:
        from_attributes = True

class ReportTextDetailResponse(BaseModel):
    report_id: int
    raw_text: str
    extraction_method: str
    extraction_quality: str
    page_count: int | None
    needs_ocr: bool

    class Config:
        from_attributes = True


class ExtractedFindingResponse(BaseModel):
    id: int
    report_id: int
    test_name: str
    value: str | None
    unit: str | None
    reference_range: str | None
    source_text: str | None

    class Config:
        from_attributes = True

class ClinicalFindingResponse(BaseModel):
    id: int
    report_id: int
    finding_text: str
    body_area: str | None
    severity: str | None
    source_section: str | None

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    report_id: int
    output_type: str
    content: str
    language: str

class SupportedLanguage(str, Enum):
    english = "English"
    hindi = "Hindi"
    kannada = "Kannada"
    tamil = "Tamil"
    telugu = "Telugu"

class ExplanationRequest(BaseModel):
    language: SupportedLanguage

class ExplanationResponse(BaseModel):
    report_id: int
    language: str
    content: str

class ChatRequest(BaseModel):
    question: str
    language: SupportedLanguage


class ChatResponse(BaseModel):
    report_id: int
    question: str
    answer: str
    language: str


class ChatHistoryResponse(BaseModel):
    id: int
    report_id: int
    question: str
    answer: str
    language: str
    created_at: datetime

    class Config:
        from_attributes = True

class AudioRequest(BaseModel):
    language: SupportedLanguage
    output_type: str = "patient_explanation"


class AudioResponse(BaseModel):
    report_id: int
    language: str
    audio_path: str
