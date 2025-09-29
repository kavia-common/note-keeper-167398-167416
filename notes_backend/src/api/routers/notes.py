from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from ..services.notes_service import NotesService
from ..models.note_models import NoteCreate, NoteUpdate, NoteOut, PaginatedNotes

router = APIRouter()

_service = NotesService()  # service encapsulates business logic and repository access


# PUBLIC_INTERFACE
@router.post(
    "/notes",
    summary="Create a note",
    description="Create a new note with title and optional content/tags.",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteOut,
    responses={
        201: {"description": "Note created successfully."},
        400: {"description": "Validation error."},
    },
)
def create_note(payload: NoteCreate) -> NoteOut:
    """
    Create a new note.

    Parameters:
      - payload: NoteCreate
        The note details including title, optional content and tags.

    Returns:
      - NoteOut: The created note.
    """
    note = _service.create_note(payload)
    return NoteOut.model_validate(note.model_dump())


# PUBLIC_INTERFACE
@router.get(
    "/notes",
    summary="List notes",
    description="List notes with optional search and pagination.",
    response_model=PaginatedNotes,
)
def list_notes(
    q: Optional[str] = Query(
        default=None,
        description="Search query to filter notes by title or content.",
    ),
    limit: int = Query(default=20, ge=1, le=100, description="Max items to return."),
    offset: int = Query(default=0, ge=0, description="Number of items to skip."),
) -> PaginatedNotes:
    """
    List notes with optional search and pagination.

    Parameters:
      - q: Optional[str] search phrase for title or content
      - limit: int number of items
      - offset: int skip count

    Returns:
      - PaginatedNotes: total count and items.
    """
    return _service.list_notes(q=q, limit=limit, offset=offset)


# PUBLIC_INTERFACE
@router.get(
    "/notes/{note_id}",
    summary="Get a note",
    description="Retrieve a note by its unique identifier.",
    response_model=NoteOut,
    responses={
        404: {"description": "Note not found."},
    },
)
def get_note(
    note_id: str = Path(..., description="The unique ID of the note."),
) -> NoteOut:
    """
    Retrieve a single note by ID.

    Parameters:
      - note_id: str unique id

    Returns:
      - NoteOut: The requested note.
    """
    note = _service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteOut.model_validate(note.model_dump())


# PUBLIC_INTERFACE
@router.put(
    "/notes/{note_id}",
    summary="Replace a note",
    description="Replace an existing note by ID with new title/content/tags.",
    response_model=NoteOut,
    responses={
        404: {"description": "Note not found."},
        400: {"description": "Validation error."},
    },
)
def replace_note(
    note_id: str = Path(..., description="The unique ID of the note."),
    payload: NoteCreate = ...,
) -> NoteOut:
    """
    Replace an existing note by ID.

    Parameters:
      - note_id: str unique id
      - payload: NoteCreate full replacement

    Returns:
      - NoteOut: updated note
    """
    note = _service.replace_note(note_id, payload)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteOut.model_validate(note.model_dump())


# PUBLIC_INTERFACE
@router.patch(
    "/notes/{note_id}",
    summary="Update a note",
    description="Partially update note fields by ID.",
    response_model=NoteOut,
    responses={
        404: {"description": "Note not found."},
        400: {"description": "Validation error."},
    },
)
def update_note(
    note_id: str = Path(..., description="The unique ID of the note."),
    payload: NoteUpdate = ...,
) -> NoteOut:
    """
    Partial update for a note.

    Parameters:
      - note_id: str unique id
      - payload: NoteUpdate fields to update

    Returns:
      - NoteOut: updated note
    """
    note = _service.update_note(note_id, payload)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteOut.model_validate(note.model_dump())


# PUBLIC_INTERFACE
@router.delete(
    "/notes/{note_id}",
    summary="Delete a note",
    description="Delete a note by its unique ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Note deleted."},
        404: {"description": "Note not found."},
    },
)
def delete_note(
    note_id: str = Path(..., description="The unique ID of the note."),
) -> None:
    """
    Delete a note by ID.

    Parameters:
      - note_id: str unique id

    Returns:
      - None: 204 on success.
    """
    deleted = _service.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
