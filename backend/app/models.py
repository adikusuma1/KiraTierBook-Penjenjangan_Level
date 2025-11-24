from pydantic import BaseModel
from typing import List, Optional

class BookRequest(BaseModel):
    title: str

class AIAnalysis(BaseModel):
    jenjang: str
    confidence_score: int
    alasan: str
    saran: str
    badge_color: str

class BookResult(BaseModel):
    title: str
    authors: List[str]
    page_count: Optional[int]
    categories: List[str]
    thumbnail: Optional[str] = None  
    screenshots: List[str]
    analysis: AIAnalysis