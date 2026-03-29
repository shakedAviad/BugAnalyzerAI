from __future__ import annotations

from ai_bug_analyzer.app.state import BugAnalyzerState
from ai_bug_analyzer.domain.enums import RunStatus
from ai_bug_analyzer.domain.models import RepairAttempt
from ai_bug_analyzer.tools.command_tools import CommandExecutionRequest, execute_command


def verify_result_node(state: BugAnalyzerState) -> dict:

    command: str | None = state.test_command or state.entry_command

    if not command:
        raise ValueError("No command was provided. Expected test_command or entry_command.")

    run_result = execute_command(CommandExecutionRequest(command=command, working_directory=state.project_path))

    attempt_history: list[RepairAttempt] = list(state.attempt_history)

    attempt_history.append(
        RepairAttempt(
            iteration=state.iteration_count,
            run_result=run_result,
            failure_classification=state.failure_classification,
            fix_plan=state.fix_plan,
            patch_result=state.patch_application_result,
        )
    )

    return {
        "current_status": RunStatus.SUCCEEDED if run_result.succeeded else RunStatus.FAILED,
        "last_run_result": run_result,
        "attempt_history": attempt_history,
        "is_resolved": run_result.succeeded,
        "should_stop": run_result.succeeded,
        "stop_reason": "Execution succeeded after patch application." if run_result.succeeded else None,
    }
