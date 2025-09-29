from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import uuid4

from ..models.note_models import Note, NoteCreate, NoteUpdate
from ..core.settings import get_app_settings


class NotesRepository(ABC):
    """Abstract repository for notes persistence."""

    @abstractmethod
    def create(self, data: NoteCreate) -> Note: ...

    @abstractmethod
    def get(self, note_id: str) -> Optional[Note]: ...

    @abstractmethod
    def list(self, q: Optional[str], limit: int, offset: int) -> Tuple[int, List[Note]]: ...

    @abstractmethod
    def replace(self, note_id: str, data: NoteCreate) -> Optional[Note]: ...

    @abstractmethod
    def update(self, note_id: str, data: NoteUpdate) -> Optional[Note]: ...

    @abstractmethod
    def delete(self, note_id: str) -> bool: ...


class InMemoryNotesRepository(NotesRepository):
    """
    Simple in-memory repository suitable for testing and development.
    """

    def __init__(self) -> None:
        self._items: dict[str, Note] = {}

    def create(self, data: NoteCreate) -> Note:
        now = datetime.utcnow()
        note = Note(
            id=str(uuid4()),
            title=data.title,
            content=data.content,
            tags=data.tags or [],
            created_at=now,
            updated_at=now,
        )
        self._items[note.id] = note
        return note

    def get(self, note_id: str) -> Optional[Note]:
        return self._items.get(note_id)

    def list(self, q: Optional[str], limit: int, offset: int) -> Tuple[int, List[Note]]:
        items = list(self._items.values())
        if q:
            q_lower = q.lower()
            items = [
                n
                for n in items
                if q_lower in n.title.lower() or (n.content and q_lower in n.content.lower())
            ]
        total = len(items)
        return total, items[offset : offset + limit]

    def replace(self, note_id: str, data: NoteCreate) -> Optional[Note]:
        if note_id not in self._items:
            return None
        now = datetime.utcnow()
        note = Note(
            id=note_id,
            title=data.title,
            content=data.content,
            tags=data.tags or [],
            created_at=self._items[note_id].created_at,
            updated_at=now,
        )
        self._items[note_id] = note
        return note

    def update(self, note_id: str, data: NoteUpdate) -> Optional[Note]:
        if note_id not in self._items:
            return None
        note = self._items[note_id]
        updated = note.model_copy(
            update={
                "title": data.title if data.title is not None else note.title,
                "content": data.content if data.content is not None else note.content,
                "tags": data.tags if data.tags is not None else note.tags,
                "updated_at": datetime.utcnow(),
            }
        )
        self._items[note_id] = updated
        return updated

    def delete(self, note_id: str) -> bool:
        return self._items.pop(note_id, None) is not None


class DatabaseNotesRepository(NotesRepository):
    """
    Placeholder for real DB repository that integrates with the `notes_database` container.
    Implement actual CRUD operations using the chosen DB driver/ORM.
    """

    def __init__(self) -> None:
        settings = get_app_settings()
        # Prepare connection info (do not open connections here)
        self._db_url = settings.db_url
        self._db_user = settings.db_user
        self._db_password = settings.db_password
        self._db_name = settings.db_name
        self._db_port = settings.db_port
        # In a real implementation, initialize engine/connection pool here.

    def create(self, data: NoteCreate) -> Note:
        raise NotImplementedError("Database integration not configured.")

    def get(self, note_id: str) -> Optional[Note]:
        raise NotImplementedError("Database integration not configured.")

    def list(self, q: Optional[str], limit: int, offset: int) -> Tuple[int, List[Note]]:
        raise NotImplementedError("Database integration not configured.")

    def replace(self, note_id: str, data: NoteCreate) -> Optional[Note]:
        raise NotImplementedError("Database integration not configured.")

    def update(self, note_id: str, data: NoteUpdate) -> Optional[Note]:
        raise NotImplementedError("Database integration not configured.")

    def delete(self, note_id: str) -> bool:
        raise NotImplementedError("Database integration not configured.")
