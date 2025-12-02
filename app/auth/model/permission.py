from core.model.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from core.mixin.int_id_ky import IntIdPk

if TYPE_CHECKING:
    from .role import Role

class Permission(Base, IntIdPk):
    __tablename__ = 'permissions'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permission_associations",
        back_populates="permissions"
    )
