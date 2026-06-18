from pathlib import Path
from gtts import gTTS
import uuid


AUDIO_DIR = "audio_outputs"

Path(AUDIO_DIR).mkdir(exist_ok=True)


LANGUAGE_TTS_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te"
}


def generate_audio_from_text(text: str, language: str):
    lang_code = LANGUAGE_TTS_MAP.get(language, "en")

    filename = f"{uuid.uuid4()}.mp3"
    file_path = f"{AUDIO_DIR}/{filename}"

    tts = gTTS(
        text=text,
        lang=lang_code
    )

    tts.save(file_path)

    return file_path