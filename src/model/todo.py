from dataclasses import dataclass
import datetime

@dataclass
class Todo:
    title: str
    createdAt: datetime
    items: list
    id: int = 0
    
    