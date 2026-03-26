from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from domain.enums import FailureType, FinalStatus


class DomainModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=False,
        use_enum_values=False,
    )


class RunResult(DomainModel):
    command: str = Field(..., min_length=1)
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    succeeded: bool
    started_at_utc: datetime
    finished_at_utc: datetime
    duration_ms: int = Field(..., ge=0)


class FailureClassification(DomainModel):
    failure_type: FailureType
    summary: str = Field(..., min_length=1)
    root_cause: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    relevant_files: list[Path] = Field(default_factory=list)
    relevant_symbols: list[str] = Field(default_factory=list)


class FileChangePlan(DomainModel):
    file_path: Path
    reason: str = Field(..., min_length=1)
    change_type: str = Field(..., min_length=1)
    target_symbol: str | None = None


class FixPlan(DomainModel):
    summary: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    changes: list[FileChangePlan] = Field(default_factory=list)
    risk_notes: list[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)


class PatchOperation(DomainModel):
    file_path: Path
    operation: str = Field(..., min_length=1)
    patch_text: str = Field(..., min_length=1)


class GeneratedPatch(DomainModel):
    summary: str = Field(..., min_length=1)
    operations: list[PatchOperation] = Field(default_factory=list)
    estimated_changed_files_count: int = Field(..., ge=0)


class PatchApplicationResult(DomainModel):
    applied: bool
    applied_files: list[Path] = Field(default_factory=list)
    failed_files: list[Path] = Field(default_factory=list)
    details: str = ""


class RepairAttempt(DomainModel):
    iteration: int = Field(..., ge=1)
    run_result: RunResult | None = None
    failure_classification: FailureClassification | None = None
    fix_plan: FixPlan | None = None
    patch_result: PatchApplicationResult | None = None


class FinalOutcome(DomainModel):
    final_status: FinalStatus
    summary: str = Field(..., min_length=1)
    total_iterations: int = Field(..., ge=0)
    resolved: bool
    changed_files: list[Path] = Field(default_factory=list)
