from app.services.llm_router import llm_router


def translation_agent(state: dict):

    if state["language"] == "English":
        state["translated_output"] = state["safe_output"]
        return state

    prompt = f"""
Translate the following text into {state['language']}.

Text:
{state['safe_output']}
"""

    translated = llm_router.generate(prompt)

    state["translated_output"] = translated

    return state