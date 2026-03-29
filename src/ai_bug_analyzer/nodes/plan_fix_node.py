from __future__ import annotations

from agents.fix_planning_agent import plan_fix
from app.state import BugAnalyzerState
from domain.schemas import FixPlanningInputSchema


def plan_fix_node(state: BugAnalyzerState) -> dict:
    last_run_result = state.last_run_result
    failure_classification = state.failure_classification

    if last_run_result is None:
        raise ValueError("Cannot plan a fix without a run result.")

    if failure_classification is None:
        raise ValueError("Cannot plan a fix without a failure classification.")

    scheme = FixPlanningInputSchema(
        project_path=state.project_path,
        command=last_run_result.command,
        failure_type=failure_classification.failure_type,
        failure_summary=failure_classification.summary,
        root_cause=failure_classification.root_cause,
        relevant_files=failure_classification.relevant_files,
        relevant_symbols=failure_classification.relevant_symbols,
        stdout=last_run_result.stdout,
        stderr=last_run_result.stderr,
    )

    return {"fix_plan": plan_fix(scheme)}
