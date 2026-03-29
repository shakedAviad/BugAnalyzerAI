from __future__ import annotations

from app.state import BugAnalyzerState
from infrastructure.persistence.checkpointing import create_in_memory_checkpointer
from langgraph.graph import END, START, StateGraph
from nodes.apply_patch_node import apply_patch_node
from nodes.classify_failure_node import classify_failure_node
from nodes.finalize_node import finalize_node
from nodes.generate_patch_node import generate_patch_node
from nodes.plan_fix_node import plan_fix_node
from nodes.run_target_node import run_target_node
from nodes.verify_result_node import verify_result_node


def should_continue_after_run(state: BugAnalyzerState) -> str:
    return "finalize" if state.is_resolved else "classify_failure"


def should_continue_after_verify(state: BugAnalyzerState) -> str:
    return "finalize" if state.is_resolved or state.iteration_count >= state.max_iterations else "classify_failure"


def build_graph():
    graph_builder = StateGraph(BugAnalyzerState)

    graph_builder.add_node("run_target", run_target_node)
    graph_builder.add_node("classify_failure", classify_failure_node)
    graph_builder.add_node("plan_fix", plan_fix_node)
    graph_builder.add_node("generate_patch", generate_patch_node)
    graph_builder.add_node("apply_patch", apply_patch_node)
    graph_builder.add_node("verify_result", verify_result_node)
    graph_builder.add_node("finalize", finalize_node)

    graph_builder.add_edge(START, "run_target")
    graph_builder.add_edge("classify_failure", "plan_fix")
    graph_builder.add_edge("plan_fix", "generate_patch")
    graph_builder.add_edge("generate_patch", "apply_patch")
    graph_builder.add_edge("apply_patch", "verify_result")
    graph_builder.add_edge("finalize", END)

    graph_builder.add_conditional_edges(
        "run_target",
        should_continue_after_run,
        {
            "classify_failure": "classify_failure",
            "finalize": "finalize",
        },
    )

    graph_builder.add_conditional_edges(
        "verify_result",
        should_continue_after_verify,
        {
            "classify_failure": "classify_failure",
            "finalize": "finalize",
        },
    )

    return graph_builder.compile(checkpointer=create_in_memory_checkpointer())
