from __future__ import annotations

from ai_bug_analyzer.agents.patch_generation_agent import generate_patch
from ai_bug_analyzer.app.state import BugAnalyzerState
from ai_bug_analyzer.domain.schemas import FileChangePlanSchema, PatchGenerationInputSchema


def generate_patch_node(state: BugAnalyzerState) -> dict:
    fix_plan = state.fix_plan

    if fix_plan is None:
        raise ValueError("Cannot generate a patch without a fix plan.")

    scheme = PatchGenerationInputSchema(
        project_path=state.project_path,
        fix_summary=fix_plan.summary,
        fix_rationale=fix_plan.rationale,
        changes=[
            FileChangePlanSchema(
                file_path=change.file_path,
                reason=change.reason,
                change_type=change.change_type,
                target_symbol=change.target_symbol,
            )
            for change in fix_plan.changes
        ],
    )

    generated_patch = generate_patch(scheme)

    return {"generated_patch": generated_patch}
