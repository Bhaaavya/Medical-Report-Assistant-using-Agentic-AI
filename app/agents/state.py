from typing import TypedDict


class MedicalAgentState(TypedDict):
    report_id: int

    report_type: str

    report_text: str

    language: str

    summary: str

    explanation: str

    safe_output: str

    translated_output: str

    audio_path: str

    question: str

    answer: str
    audio_path: str
