from dataclasses import dataclass
import datetime

from model.tag import Tag

@dataclass
class Note:
    title: str
    content: str
    createdAt: datetime
    tag: Tag = None
    id: int = 0
    