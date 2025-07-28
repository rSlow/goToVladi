from abc import ABC, abstractmethod
from typing import Any


class ActionableButtonProtocol(ABC):
    @abstractmethod
    def action(self, child_of_target: Any) -> None: ...
