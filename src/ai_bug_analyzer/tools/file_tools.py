from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class FileReadRequest:
    project_root: Path
    file_path: Path
    encoding: str = "utf-8"


@dataclass(slots=True, frozen=True)
class FileWriteRequest:
    project_root: Path
    file_path: Path
    content: str
    encoding: str = "utf-8"


def _resolve_project_path(project_root: Path, file_path: Path) -> Path:
    resolved_project_root: Path = project_root.resolve()
    resolved_file_path: Path = (
        file_path.resolve()
        if file_path.is_absolute()
        else (resolved_project_root / file_path).resolve()
    )

    try:
        resolved_file_path.relative_to(resolved_project_root)
    except ValueError as error:
        raise ValueError("File path is outside the project root.") from error

    return resolved_file_path


def read_text_file(request: FileReadRequest) -> str:
    resolved_file_path: Path = _resolve_project_path(
        project_root=request.project_root,
        file_path=request.file_path,
    )

    return resolved_file_path.read_text(encoding=request.encoding)


def write_text_file(request: FileWriteRequest) -> None:
    resolved_file_path: Path = _resolve_project_path(
        project_root=request.project_root,
        file_path=request.file_path,
    )

    resolved_file_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_file_path.write_text(request.content, encoding=request.encoding)
