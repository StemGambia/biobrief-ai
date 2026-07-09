from dataclasses import dataclass, field
from typing import List


@dataclass
class SearchTask:
    query: str
    purpose: str


@dataclass
class Mission:

    user_goal: str

    objective: str

    search_tasks: List[SearchTask] = field(default_factory=list)

    information_needed: List[str] = field(default_factory=list)

    priority: str = "Medium"

    status: str = "Planning"
