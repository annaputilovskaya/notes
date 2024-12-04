from fastapi.security import HTTPBearer
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from notices import crud
from notices.dependencies import note_by_id
from notices.models import Note
from notices.schemas import NoteDetailSchema, NoteSchema, NoteUpdateSchema
from users.dependencies import current_active_verified_user
from users.models.user import User

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/notes",
    tags=["Заметки"],
    dependencies=[Depends(http_bearer)],
)


@router.post(
    "",
    summary="Создать заметку",
    response_model=NoteDetailSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note: NoteSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_verified_user),
):
    return await crud.add_note(note_in=note, session=session, user=user)


@router.get("", summary="Все заметки", response_model=list[NoteDetailSchema])
async def get_notes(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_verified_user),
):
    return await crud.get_all_notes(session=session, user=user)


@router.get("/tag", summary="Заметки по тегу", response_model=list[NoteDetailSchema])
async def get_notes_by_tag(
    tag: str,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_verified_user),
):
    return await crud.get_notes_by_tag(session=session, input_tag=tag, user=user)


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
