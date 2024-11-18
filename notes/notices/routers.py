from core.database import db_helper
from fastapi import APIRouter, Depends, status
from notices import crud
from notices.dependencies import note_by_id
from notices.models import Note
from notices.schemas import NoteDetailSchema, NoteSchema, NoteUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/notes", tags=["Заметки"])


@router.post(
    "",
    summary="Создать заметку",
    response_model=NoteDetailSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note: NoteSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.add_note(note_in=note, session=session)


@router.get("", summary="Все заметки", response_model=list[NoteDetailSchema])
async def get_notes(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_all_notes(session=session)


@router.get("/tag", summary="Заметки по тегу", response_model=list[NoteDetailSchema])
async def get_notes_by_tag(
    tag: str, session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.get_notes_by_tag(session=session, input_tag=tag)


@router.get("/{note_id}", summary="Заметка по id", response_model=NoteDetailSchema)
async def get_note(note: Note = Depends(note_by_id)):
    return note


@router.patch("/{note_id}", summary="Изменить заметку", response_model=NoteDetailSchema)
async def update_note(
    note_in: NoteUpdateSchema,
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_note(session=session, note=note, note_in=note_in)


@router.delete(
    "/{note_id}", summary="Удалить заметку", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_note(
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.delete_note(session=session, note=note)
