from __future__ import annotations

from app.state import BugAnalyzerState
from domain.enums import RunStatus
from tools.command_tools import CommandExecutionRequest, execute_command


def run_target_node(state: BugAnalyzerState) -> dict:
    command: str | None = state.test_command or state.entry_command

    if not command:
        raise ValueError("No command was provided. Expected test_command or entry_command.")

    request = CommandExecutionRequest(command=command, working_directory=state.project_path)
    run_result = execute_command(request)

    return {
        "iteration_count": state.iteration_count + 1,
        "current_status": RunStatus.SUCCEEDED if run_result.succeeded else RunStatus.FAILED,
        "last_run_result": run_result,
        "is_resolved": run_result.succeeded,
        "should_stop": run_result.succeeded,
        "stop_reason": "Execution succeeded." if run_result.succeeded else None,
    }
