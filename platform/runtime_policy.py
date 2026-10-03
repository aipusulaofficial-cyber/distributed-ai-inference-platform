"""Fail-closed inference runtime policy."""


def validate(
    timeout_seconds: float, attempts: int, max_timeout: float = 30, max_attempts: int = 2
) -> bool:
    return 0 < timeout_seconds <= max_timeout and 1 <= attempts <= max_attempts
