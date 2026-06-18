from app.services.llm_router import llm_router


def safety_agent(state: dict):

    prompt = f"""
You are a medical safety reviewer.

Review the following response.

Response:
{state["explanation"]}

Tasks:
1. Remove any diagnosis claims.
2. Remove any medication recommendations.
3. Remove any treatment recommendations.
4. Remove any emergency instructions unless explicitly present in report.
5. Keep the explanation educational.
6. Add a disclaimer at the end.

Return only the corrected response.
"""

    safe_output = llm_router.generate(prompt)

    state["safe_output"] = safe_output

    return state