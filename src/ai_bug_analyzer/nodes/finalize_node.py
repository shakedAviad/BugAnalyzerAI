from __future__ import annotations

from ai_bug_analyzer.app.state import BugAnalyzerState
from ai_bug_analyzer.domain.enums import FinalStatus
from ai_bug_analyzer.domain.models import FinalOutcome


def finalize_node(state: BugAnalyzerState) -> dict:
    if state.is_resolved:
        final_status = FinalStatus.RESOLVED
        summary = "Bug analysis flow completed successfully."
    elif state.should_stop:
        final_status = FinalStatus.STOPPED
        summary = state.stop_reason or "Bug analysis flow stopped."
    else:
        final_status = FinalStatus.FAILED
        summary = "Bug analysis flow ended without resolving the issue."

    final_outcome = FinalOutcome(
        final_status=final_status,
        summary=summary,
        total_iterations=state.iteration_count,
        resolved=state.is_resolved,
        changed_files=state.changed_files,
    )

    return {"final_outcome": final_outcome, "current_status": state.current_status, "should_stop": True}
