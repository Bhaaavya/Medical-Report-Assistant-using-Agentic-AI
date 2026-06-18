from app.services.llm_router import llm_router


def explanation_agent(state: dict):

    prompt = f"""
Explain the following medical summary in simple
{state['language']} language.

Summary:
{state['summary']}

Rules:
- Use simple language.
- Do not diagnose.
- Do not prescribe treatment.
- Explain for a non-medical person.
"""

    explanation = llm_router.generate(prompt)

    state["explanation"] = explanation

    return state