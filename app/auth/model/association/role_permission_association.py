from core.model.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class RolePermissionAssociation(Base):
    __tablename__ = "role_permission_associations"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )
