from typing import Annotated

from core import db_helper
from fastapi import Depends, HTTPException, Path, status
from notices.crud import get_note
from notices.models import Note
from sqlalchemy.ext.asyncio import AsyncSession


async def note_by_id(
    note_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Note:
    """
    Получение заметки по ее идентификатору.
    """

    note = await get_note(session=session, note_id=note_id)
    if note is not None:
        return note

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Note {note_id} not found!",
    )
