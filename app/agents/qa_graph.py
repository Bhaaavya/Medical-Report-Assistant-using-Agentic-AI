from langgraph.graph import StateGraph, END

from app.agents.state import MedicalAgentState
from app.agents.qa_agent import qa_agent


builder = StateGraph(MedicalAgentState)

builder.add_node("qa_agent", qa_agent)

builder.set_entry_point("qa_agent")

builder.add_edge("qa_agent", END)

qa_graph = builder.compile()