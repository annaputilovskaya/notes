from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class TagSchema(BaseModel):
    """
    Базовая схема тега заметки.
    """

    name: str = Field(title="name", max_length=36, pattern="#\w+")


class TagDetailSchema(TagSchema):
    """
    Детальная схема отображения тега заметки.
    """

    id: int


class NoteSchema(BaseModel):
    """
    Базовая схема заметки.
    """

    title: str = Field(title="title", max_length=100)
    text: str = Field(title="text")
    tags: List[TagSchema] | None = None


class NoteDetailSchema(NoteSchema):
    """
    Детальная схема отображения заметки с тегами.
    """

    id: int
    created_at: datetime = Field(title="created_at")
    updated_at: datetime = Field(title="updated_at")
    tags: List[TagSchema]


class NoteUpdateSchema(BaseModel):
    """
    Схема изменения заметки.
    """

    title: str | None = None
    text: str | None = None
    tags: List[TagSchema] | None = None
