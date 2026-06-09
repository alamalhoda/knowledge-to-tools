from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseEmitter(ABC):
    """
    Base class for all emitters in Aegis v2.
    Each emitter receives IR (tool-neutral) and translates it into tool-specific output.
    """

    def __init__(self, ir: Dict[str, Any]):
        if not isinstance(ir, dict):
            raise ValueError("Emitter received invalid IR.")
        self.ir = ir

    @abstractmethod
    def emit(self) -> None:
        pass
