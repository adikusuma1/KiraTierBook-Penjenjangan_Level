from pydantic import BaseModel
from typing import List, Optional


class BookRequest(BaseModel):
    title: str


class BookData(BaseModel):
    title: str
    authors: List[str]
    page_count: Optional[int]
    categories: List[str]
    screenshots: List[str]