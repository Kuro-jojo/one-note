from dataclasses import dataclass
import datetime

from model.tag import Tag

@dataclass
class Note:
    title: str
    content: str
    createdAt: datetime
    id: int = 0
    