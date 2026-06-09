from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional

from ir.models import IRRoot


class BaseEmitter(ABC):
    """
    Base class for all emitters in Aegis v2.
    Each emitter receives IRRoot and translates it into tool-specific output.
    """

    BASE_DIR: Path = Path(".")

    @abstractmethod
    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        pass

    def _resolve_output_dir(self, output_dir: Optional[Path] = None) -> Path:
        if output_dir is not None:
            return output_dir
        return self.BASE_DIR

    def _ir_to_dict(self, ir: IRRoot) -> Dict[str, Any]:
        return ir.to_dict()
