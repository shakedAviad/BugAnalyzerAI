from __future__ import annotations

from ai_bug_analyzer.agents.failure_classification_agent import classify_failure
from ai_bug_analyzer.app.state import BugAnalyzerState
from ai_bug_analyzer.domain.schemas import FailureClassificationInputSchema


def classify_failure_node(state: BugAnalyzerState) -> dict:
    last_run_result = state.last_run_result

    if last_run_result is None:
        raise ValueError("Cannot classify failure without a run result.")

    if last_run_result.succeeded:
        return {}

    schema = FailureClassificationInputSchema(
        project_path=state.project_path,
        command=last_run_result.command,
        exit_code=last_run_result.exit_code,
        stdout=last_run_result.stdout,
        stderr=last_run_result.stderr,
    )

    failure_classification = classify_failure(schema)

    return {"failure_classification": failure_classification}
