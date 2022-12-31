from dataclasses import dataclass
import datetime

from model.todo import Todo

@dataclass
class Item:
    title: str
    todo: Todo    
    id: int = 0
    