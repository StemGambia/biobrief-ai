from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Paper:

    pmid: str

    title: str

    abstract: str


@dataclass
class ResearchPackage:

    mission: str

    searches_executed: List[str]

    papers: List[Paper] = field(default_factory=list)

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    @property
    def paper_count(self):

        return len(self.papers)
