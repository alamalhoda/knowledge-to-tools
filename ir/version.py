from __future__ import annotations

from typing import List


IR_VERSION = "2.0"
SUPPORTED_VERSIONS: List[str] = ["1.0", "2.0"]


def check_version(version: str) -> bool:
    """Check if an IR version is supported."""
    return version in SUPPORTED_VERSIONS


def raise_if_unsupported(version: str) -> None:
    """Raise an error if the IR version is not supported."""
    if not check_version(version):
        raise UnsupportedIRVersionError(
            f"IR version '{version}' is not supported. "
            f"Supported versions: {SUPPORTED_VERSIONS}"
        )


class UnsupportedIRVersionError(Exception):
    """Raised when an unsupported IR version is encountered."""
    pass
