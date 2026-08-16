from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Holiday:
    date: date
    name: str
    category: str = "public"
    source: str | None = None