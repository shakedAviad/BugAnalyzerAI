from __future__ import annotations

from pathlib import Path

from agents.patch_generation_agent import generate_patch
from app.state import BugAnalyzerState
from domain.schemas import FileChangePlanSchema, PatchGenerationInputSchema


def generate_patch_node(state: BugAnalyzerState) -> dict:
    fix_plan = state.fix_plan

    if fix_plan is None:
        raise ValueError("Cannot generate a patch without a fix plan.")

    enriched_changes = []

    for change in fix_plan.changes:
        full_path = Path(state.project_path) / change.file_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")

        original_content = full_path.read_text()

        enriched_changes.append(
            FileChangePlanSchema(
                file_path=change.file_path,
                reason=change.reason,
                change_type=change.change_type,
                target_symbol=change.target_symbol,
                original_content=original_content,
            )
        )

    scheme = PatchGenerationInputSchema(
        project_path=state.project_path,
        fix_summary=fix_plan.summary,
        fix_rationale=fix_plan.rationale,
        changes=enriched_changes,
    )

    return {"generated_patch": generate_patch(scheme)}
