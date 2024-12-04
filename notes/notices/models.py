from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from core.mixins.id_int_pk_mixin import IdIntPkMixin


class NoteTagAssociation(Base, IdIntPkMixin):
    """
    Модель взаимосвязи заметки с тегами в базе данных.
    """

    __tablename__ = "note_tag_association"
    __table_args__ = (
        UniqueConstraint("note_id", "tag_id", name="idx_unique_note_tag"),
    )

    note_id: Mapped[int] = mapped_column(
        ForeignKey("note.id", ondelete="CASCADE"),
    )
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE"))


class Note(Base, IdIntPkMixin):
    """
    Модель заметки для отображения в базе данных.
    """

    title: Mapped[str]
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    tags: Mapped[List["Tag"]] = relationship(
        secondary="note_tag_association",
        back_populates="notes",
    )
    owner: Mapped[int | None] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id=}, {self.title=}, {self.tags=})"


class Tag(Base, IdIntPkMixin):
    """
    Модель тега заметки для отображения в базе данных.
    """

    name: Mapped[str] = mapped_column(unique=True)
    notes: Mapped[List["Note"]] = relationship(
        secondary="note_tag_association",
        back_populates="tags",
        cascade="delete",
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id=}, {self.name=})"
