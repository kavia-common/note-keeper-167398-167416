from typing import Optional

from ..models.note_models import NoteCreate, NoteUpdate, Note, PaginatedNotes
from ..repositories.notes_repository import (
    InMemoryNotesRepository,
    NotesRepository,
    DatabaseNotesRepository,
)
from ..core.settings import get_app_settings


class NotesService:
    """Business logic for managing notes."""

    def __init__(self, repository: NotesRepository | None = None) -> None:
        if repository:
            self.repo = repository
        else:
            # Select DB repo only if configured; otherwise use in-memory.
            settings = get_app_settings()
            if settings.db_url:
                # Wire up DB repository if environment is provided.
                self.repo = DatabaseNotesRepository()
            else:
                self.repo = InMemoryNotesRepository()

    # PUBLIC_INTERFACE
    def create_note(self, payload: NoteCreate) -> Note:
        """Create a note and return the created entity."""
        return self.repo.create(payload)

    # PUBLIC_INTERFACE
    def get_note(self, note_id: str) -> Optional[Note]:
        """Retrieve a note by its unique identifier."""
        return self.repo.get(note_id)

    # PUBLIC_INTERFACE
    def list_notes(self, q: Optional[str], limit: int, offset: int) -> PaginatedNotes:
        """Return a paginated list of notes filtered by optional search query."""
        total, items = self.repo.list(q=q, limit=limit, offset=offset)
        return PaginatedNotes(total=total, items=items)

    # PUBLIC_INTERFACE
    def replace_note(self, note_id: str, payload: NoteCreate) -> Optional[Note]:
        """Replace an existing note with new data."""
        return self.repo.replace(note_id, payload)

    # PUBLIC_INTERFACE
    def update_note(self, note_id: str, payload: NoteUpdate) -> Optional[Note]:
        """Partially update note data."""
        return self.repo.update(note_id, payload)

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: str) -> bool:
        """Delete a note by ID."""
        return self.repo.delete(note_id)
