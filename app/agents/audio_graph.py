from langgraph.graph import StateGraph, END

from app.agents.state import MedicalAgentState

from app.agents.intake_agent import intake_agent
from app.agents.summary_agent import summary_agent
from app.agents.explanation_agent import explanation_agent
from app.agents.safety_agent import safety_agent
from app.agents.translation_agent import translation_agent
from app.agents.audio_agent import audio_agent


builder = StateGraph(MedicalAgentState)

builder.add_node("intake_agent", intake_agent)
builder.add_node("summary_agent", summary_agent)
builder.add_node("explanation_agent", explanation_agent)
builder.add_node("safety_agent", safety_agent)
builder.add_node("translation_agent", translation_agent)
builder.add_node("audio_agent", audio_agent)

builder.set_entry_point("intake_agent")

builder.add_edge("intake_agent", "summary_agent")
builder.add_edge("summary_agent", "explanation_agent")
builder.add_edge("explanation_agent", "safety_agent")
builder.add_edge("safety_agent", "translation_agent")
builder.add_edge("translation_agent", "audio_agent")
builder.add_edge("audio_agent", END)

audio_graph = builder.compile()