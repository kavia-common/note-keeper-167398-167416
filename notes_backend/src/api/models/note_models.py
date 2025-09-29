from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., description="Short title for the note.", max_length=200)
    content: Optional[str] = Field(None, description="Detailed content of the note.")
    tags: List[str] = Field(default_factory=list, description="Tags for organization.")


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated title.", max_length=200)
    content: Optional[str] = Field(None, description="Updated content.")
    tags: Optional[List[str]] = Field(None, description="Updated tags.")


class Note(NoteBase):
    id: str = Field(..., description="Unique identifier for the note.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")


class NoteOut(Note):
    pass


class PaginatedNotes(BaseModel):
    total: int = Field(..., description="Total number of matching notes.")
    items: List[NoteOut] = Field(..., description="List of notes in current page.")
