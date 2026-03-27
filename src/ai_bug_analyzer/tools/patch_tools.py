from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_bug_analyzer.tools.file_tools import (
    FileReadRequest,
    FileWriteRequest,
    read_text_file,
    write_text_file,
)


@dataclass(slots=True, frozen=True)
class ReplaceFileContentRequest:
    project_root: Path
    file_path: Path
    new_content: str


@dataclass(slots=True, frozen=True)
class ReplaceTextInFileRequest:
    project_root: Path
    file_path: Path
    old_text: str
    new_text: str
    expected_replacements: int | None = 1


def replace_file_content(request: ReplaceFileContentRequest) -> None:
    write_text_file(
        FileWriteRequest(
            project_root=request.project_root,
            file_path=request.file_path,
            content=request.new_content,
        )
    )


def replace_text_in_file(request: ReplaceTextInFileRequest) -> None:
    current_content: str = read_text_file(
        FileReadRequest(
            project_root=request.project_root,
            file_path=request.file_path,
        )
    )

    replacement_count: int = current_content.count(request.old_text)

    if replacement_count == 0:
        raise ValueError("The target text was not found in the file.")

    if (
        request.expected_replacements is not None
        and replacement_count != request.expected_replacements
    ):
        raise ValueError(
            f"Expected {request.expected_replacements} replacements, but found {replacement_count} matches."
        )

    updated_content: str = current_content.replace(request.old_text, request.new_text)

    write_text_file(
        FileWriteRequest(
            project_root=request.project_root,
            file_path=request.file_path,
            content=updated_content,
        )
    )
