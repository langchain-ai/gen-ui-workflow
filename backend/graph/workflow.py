"""
Workflow graph for recursive idea-based component generation with map-reduce.
"""

from langgraph.graph import StateGraph, START, END
from .state import GraphState
from .nodes import expand_component, should_continue_expansion

builder = StateGraph(GraphState)

builder.add_node("expand_component", expand_component)

builder.add_edge(START, "expand_component")
builder.add_conditional_edges(
    "expand_component",
    should_continue_expansion,
)

genui_graph = builder.compile()
