from pydantic import BaseModel
from typing import List, Optional

class Note(BaseModel):
    title: str
    content: str  # Raw markdown content
    file_path: str

class Theme(BaseModel):
    title: str
    notes: List[Note]
    intro_note: Optional[Note] = None

class Block(BaseModel):
    title: str
    themes: List[Theme]
    direct_notes: List[Note]  # Notes directly under block (if any)
