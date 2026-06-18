from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL, DEFAULT_LLM_PROVIDER


class LLMRouter:
    def __init__(self):
        self.default_provider = DEFAULT_LLM_PROVIDER

        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing")

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(self, prompt: str, provider: str | None = None):
        selected_provider = provider or self.default_provider

        if selected_provider == "gemini":
            return self._generate_with_gemini(prompt)

        if selected_provider == "openai":
            raise NotImplementedError("OpenAI support will be added later")

        if selected_provider == "claude":
            raise NotImplementedError("Claude support will be added later")

        raise ValueError(f"Unsupported LLM provider: {selected_provider}")

    def _generate_with_gemini(self, prompt: str):
        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text


llm_router = LLMRouter()