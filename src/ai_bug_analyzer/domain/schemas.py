from __future__ import annotations

from pathlib import Path

from domain.enums import FailureType
from pydantic import BaseModel, ConfigDict, Field


class AgentSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True, arbitrary_types_allowed=False, use_enum_values=False)


class FailureClassificationInputSchema(AgentSchema):
    project_path: Path
    command: str = Field(..., min_length=1)
    exit_code: int
    stdout: str = ""
    stderr: str = ""


class FailureClassificationOutputSchema(AgentSchema):
    failure_type: FailureType
    summary: str = Field(..., min_length=1)
    root_cause: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    relevant_files: list[Path] = Field(default_factory=list)
    relevant_symbols: list[str] = Field(default_factory=list)


class FixPlanningInputSchema(AgentSchema):
    project_path: Path
    command: str = Field(..., min_length=1)
    failure_type: FailureType
    failure_summary: str = Field(..., min_length=1)
    root_cause: str = Field(..., min_length=1)
    relevant_files: list[Path] = Field(default_factory=list)
    relevant_symbols: list[str] = Field(default_factory=list)
    stdout: str = ""
    stderr: str = ""


class FileChangePlanSchema(AgentSchema):
    file_path: Path
    reason: str = Field(..., min_length=1)
    change_type: str = Field(..., min_length=1)
    target_symbol: str | None = (None,)
    original_content: str = Field(..., min_length=1)


class FixPlanningOutputSchema(AgentSchema):
    summary: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    changes: list[FileChangePlanSchema] = Field(default_factory=list)
    risk_notes: list[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)


class PatchGenerationInputSchema(AgentSchema):
    project_path: Path
    fix_summary: str = Field(..., min_length=1)
    fix_rationale: str = Field(..., min_length=1)
    changes: list[FileChangePlanSchema] = Field(default_factory=list)


class PatchOperationSchema(AgentSchema):
    file_path: Path
    operation: str = Field(..., min_length=1)
    patch_text: str = Field(..., min_length=1)


class PatchGenerationOutputSchema(AgentSchema):
    summary: str = Field(..., min_length=1)
    operations: list[PatchOperationSchema] = Field(default_factory=list)
    estimated_changed_files_count: int = Field(..., ge=0)
