from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Locator:
    strategy: str
    value: str
    description: str = ""

    def as_tuple(self) -> Tuple[str, str]:
        return self.strategy, self.value

    @property
    def display_name(self) -> str:
        return self.description or f"{self.strategy}={self.value}"
