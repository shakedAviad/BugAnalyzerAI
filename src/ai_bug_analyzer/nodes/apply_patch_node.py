from __future__ import annotations

from pathlib import Path

from app.state import BugAnalyzerState
from domain.models import PatchApplicationResult
from tools.patch_tools import ReplaceFileContentRequest, replace_file_content


def apply_patch_node(state: BugAnalyzerState) -> dict:
    generated_patch = state.generated_patch

    if generated_patch is None:
        raise ValueError("Cannot apply a patch without a generated patch.")

    applied_files: list[Path] = []
    failed_files: list[Path] = []

    for operation in generated_patch.operations:
        try:
            replace_file_content(
                ReplaceFileContentRequest(
                    project_root=state.project_path,
                    file_path=operation.file_path,
                    new_content=operation.patch_text,
                )
            )
            applied_files.append(operation.file_path)
        except Exception:
            failed_files.append(operation.file_path)

    patch_application_result = PatchApplicationResult(
        applied=len(failed_files) == 0,
        applied_files=applied_files,
        failed_files=failed_files,
        details="Patch applied successfully." if not failed_files else "Patch was applied partially.",
    )

    updated_changed_files: list[Path] = list(state.changed_files)
    updated_changed_files.extend(file_path for file_path in applied_files if file_path not in updated_changed_files)

    return {
        "patch_application_result": patch_application_result,
        "changed_files": updated_changed_files,
    }
