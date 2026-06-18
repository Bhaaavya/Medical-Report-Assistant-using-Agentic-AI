from app.services.llm_router import llm_router


def summary_agent(state: dict):

    prompt = f"""
You are a medical report assistant.

Create a concise clinical summary.

Report Type:
{state['report_type']}

Report Text:
{state['report_text'][:5000]}

Rules:
- Do not diagnose.
- Do not prescribe treatment.
- Create a doctor-style summary.
"""

    summary = llm_router.generate(prompt)

    state["summary"] = summary

    return state