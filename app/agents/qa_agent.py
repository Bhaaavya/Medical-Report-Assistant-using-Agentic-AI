from app.services.llm_router import llm_router


def qa_agent(state: dict):
    prompt = f"""
You are a safe medical report question-answering assistant.

Answer the user's question in simple language.

User Question:
{state["question"]}

Report Type:
{state["report_type"]}

Report Text:
{state["report_text"][:5000]}

Rules:
- Answer only from the uploaded report.
- If the answer is not in the report, say it is not mentioned.
- Do not diagnose.
- Do not prescribe medicine.
- Tell the user to consult a qualified doctor.
- If it is a veterinary report, say veterinarian.
"""

    answer = llm_router.generate(prompt)

    state["answer"] = answer

    return state