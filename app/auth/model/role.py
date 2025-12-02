from core.model.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from core.mixin.int_id_ky import IntIdPk

if TYPE_CHECKING:
    from .permission import Permission
    from .user import User

class Role(Base, IntIdPk):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    # already exists
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_role_associations",
        back_populates="roles"
    )

    # add this ↓↓↓
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="role_permission_associations",
        back_populates="roles"
    )
