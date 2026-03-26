from __future__ import annotations

from pathlib import Path

from pydantic import Field

from ai_bug_analyzer.domain.enums import RunStatus
from ai_bug_analyzer.domain.models import (
    DomainModel,
    FailureClassification,
    FinalOutcome,
    FixPlan,
    GeneratedPatch,
    PatchApplicationResult,
    RepairAttempt,
    RunResult,
)


class BugAnalyzerState(DomainModel):
    project_path: Path  # root path of the analyzed project
    entry_command: str | None = None  # optional run command
    test_command: str | None = None  # optional test command (e.g. pytest)

    iteration_count: int = Field(default=0, ge=0)  # current loop iteration
    max_iterations: int = Field(default=3, ge=1)  # max allowed iterations

    current_status: RunStatus = RunStatus.PENDING  # current execution status
    last_run_result: RunResult | None = None  # last command execution result
    failure_classification: FailureClassification | None = None  # detected failure type
    fix_plan: FixPlan | None = None  # planned fix strategy
    generated_patch: GeneratedPatch | None = None  # generated code patch
    patch_application_result: PatchApplicationResult | None = (
        None  # patch apply outcome
    )

    changed_files: list[Path] = Field(default_factory=list)  # files modified so far
    attempt_history: list[RepairAttempt] = Field(
        default_factory=list
    )  # history of attempts
    final_outcome: FinalOutcome | None = None  # final result summary

    is_resolved: bool = False  # indicates success
    should_stop: bool = False  # stop execution flag
    stop_reason: str | None = None  # reason for stopping
