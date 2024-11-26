from typing import List, Set

from notices.models import Note, Tag
from notices.schemas import NoteSchema, NoteUpdateSchema, TagSchema
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


def create_note(
    note: NoteSchema,
) -> Note:
    """
    Создает заметку.
    """

    new_note = Note(title=note.title, text=note.text)
    return new_note


def create_tag(
    tag: TagSchema,
) -> Tag:
    """
    Создает тег.
    """

    new_tag = Tag(**tag.model_dump())
    return new_tag


async def get_tags_by_name(session: AsyncSession, names: Set[str]) -> List[Tag]:
    """
    Получает теги по именам тегов.
    """

    stmt = select(Tag).where(or_(Tag.name == name for name in names))
    tags = await session.scalars(stmt)
    return list(tags)


async def get_tags_to_append(session: AsyncSession, tags: List[TagSchema]) -> List[Tag]:
    """
    Получает список тегов для добавления к заметке.
    """

    if tags:
        names = set([tag.name for tag in tags])
        tags_to_append = await get_tags_by_name(session, names)
        found_names = [tag.name for tag in tags_to_append if tags_to_append]
        for tag in tags:
            if tag.name not in found_names:
                new_tag = create_tag(tag=tag)
                session.add(new_tag)
                await session.commit()
                await session.refresh(new_tag)
                tags_to_append.append(new_tag)

        return tags_to_append
    return []


async def add_note(
    session: AsyncSession,
    note_in: NoteSchema,
) -> Note:
    """
    Добавляет заметку с тегами в базу данных.
    """

    tags = await get_tags_to_append(session=session, tags=note_in.tags)
    new_note = create_note(note_in)
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    note = await get_note(session=session, note_id=new_note.id)
    note.tags += tags
    await session.commit()
    return note


async def get_all_notes(session: AsyncSession) -> list[Note]:
    """
    Получает информацию о всех заметках вместе с информацией о тегах.
    """

    stmt = (
        select(Note)
        .options(
            selectinload(Note.tags),
        )
        .order_by(Note.id)
    )
    notes = await session.scalars(stmt)

    return list(notes)


async def get_note(session: AsyncSession, note_id: int) -> Note | None:
    """
    Получает информацию о заметке по ее идентификатору вместе с информацией о тегах.
    """

    return await session.scalar(
        select(Note)
        .where(Note.id == note_id)
        .options(
            selectinload(Note.tags),
        ),
    )


async def get_notes_by_tag(session: AsyncSession, input_tag: str) -> list[Note]:
    """
    Получает информацию о заметках, содержащих определенный тег.
    """

    stmt = (
        select(Note)
        .join(Note.tags)
        .options(selectinload(Note.tags))
        .where(Tag.name == input_tag)
    )
    notes = await session.scalars(stmt)
    return list(notes)


async def delete_note(session: AsyncSession, note: Note) -> dict[str:str]:
    """
    Удаляет заметку.
    """

    await session.delete(note)
    await session.commit()
    return {"detail": "Note deleted."}


async def update_note(
    session: AsyncSession, note: Note, note_in: NoteUpdateSchema
) -> Note:
    """
    Изменяет заметку.
    """

    note_dict = note_in.model_dump(exclude_unset=True)
    if "tags" in note_dict:
        note.tags = []
        tags = await get_tags_to_append(session=session, tags=note_in.tags)
        del note_dict["tags"]
        if tags:
            note.tags += tags
    for name, value in note_dict.items():
        setattr(note, name, value)

    await session.commit()
    return note
