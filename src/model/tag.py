from dataclasses import dataclass, field
import datetime

@dataclass
class Tag:
    title: str
    color: str
    notes: list = field(default_factory=list)
    id: int = 0    