from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from domain.models import RunResult


@dataclass(slots=True, frozen=True)
class CommandExecutionRequest:
    command: str
    working_directory: Path
    timeout_seconds: int = 300


def execute_command(request: CommandExecutionRequest) -> RunResult:
    started_at_monotonic: float = time.monotonic()
    started_at_utc: datetime = datetime.now(UTC)

    completed_process = subprocess.run(
        request.command,
        cwd=request.working_directory,
        shell=True,
        capture_output=True,
        text=True,
        timeout=request.timeout_seconds,
        check=False,
    )

    finished_at_utc: datetime = datetime.now(UTC)
    duration_ms: int = int((time.monotonic() - started_at_monotonic) * 1000)

    return RunResult(
        command=request.command,
        exit_code=completed_process.returncode,
        stdout=completed_process.stdout or "",
        stderr=completed_process.stderr or "",
        succeeded=completed_process.returncode == 0,
        started_at_utc=started_at_utc,
        finished_at_utc=finished_at_utc,
        duration_ms=duration_ms,
    )
