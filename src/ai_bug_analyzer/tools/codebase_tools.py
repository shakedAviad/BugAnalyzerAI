from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIRECTORIES: tuple[str, ...] = (
    ".git",
    ".idea",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
)


@dataclass(slots=True, frozen=True)
class ListProjectFilesRequest:
    project_root: Path
    include_extensions: tuple[str, ...] = (".py",)


@dataclass(slots=True, frozen=True)
class SearchInCodebaseRequest:
    project_root: Path
    search_text: str
    include_extensions: tuple[str, ...] = (".py",)


def is_valid_project_path(file_path: Path, include_extensions: tuple[str, ...]) -> bool:
    return file_path.is_file() and not (
        any(excluded_part in file_path.parts for excluded_part in EXCLUDED_DIRECTORIES)
        or (include_extensions and file_path.suffix not in include_extensions)
    )


def list_project_files(request: ListProjectFilesRequest) -> list[Path]:
    project_root: Path = request.project_root.resolve()
    result: list[Path] = []

    for file_path in project_root.rglob("*"):
        if is_valid_project_path(file_path, request.include_extensions):
            result.append(file_path.relative_to(project_root))

    return sorted(result)


def search_in_codebase(request: SearchInCodebaseRequest) -> list[Path]:
    project_root: Path = request.project_root.resolve()
    matched_files: list[Path] = []

    for file_path in list_project_files(
        ListProjectFilesRequest(
            project_root=project_root,
            include_extensions=request.include_extensions,
        )
    ):
        absolute_file_path: Path = project_root / file_path
        content: str = absolute_file_path.read_text(encoding="utf-8")

        if request.search_text in content:
            matched_files.append(file_path)

    return matched_files
