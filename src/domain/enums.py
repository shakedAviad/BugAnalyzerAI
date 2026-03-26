from enum import StrEnum


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class FailureType(StrEnum):
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    DEPENDENCY_ERROR = "dependency_error"
    CONFIG_ERROR = "config_error"
    TEST_FAILURE = "test_failure"
    LINT_FAILURE = "lint_failure"
    TYPE_CHECK_FAILURE = "type_check_failure"
    RUNTIME_EXCEPTION = "runtime_exception"
    UNKNOWN = "unknown"


class PatchStatus(StrEnum):
    NOT_GENERATED = "not_generated"
    GENERATED = "generated"
    APPLIED = "applied"
    FAILED_TO_APPLY = "failed_to_apply"


class FinalStatus(StrEnum):
    RESOLVED = "resolved"
    FAILED = "failed"
    STOPPED = "stopped"
