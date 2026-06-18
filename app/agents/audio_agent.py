from app.services.tts_service import generate_audio_from_text


def audio_agent(state: dict):

    audio_path = generate_audio_from_text(
        text=state["translated_output"],
        language=state["language"]
    )

    state["audio_path"] = audio_path

    return state