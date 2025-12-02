from core.model.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.mixin.int_id_ky import IntIdPk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role

class User(Base, IntIdPk):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    roles: Mapped[list['Role']] = relationship(
        'Role',
        secondary='user_role_associations',
        back_populates='users'
    )
