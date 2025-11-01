from pydantic import BaseModel
from typing import List, Optional

class TriageResult(BaseModel):
    incidentId: str
    tldr: str
    signals: List[str] = []
    hypotheses: List[str] = []
    next_actions: List[str] = []
    status_update: Optional[str] = ""
