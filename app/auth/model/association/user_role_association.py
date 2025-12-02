from core.model.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class UserRoleAssociation(Base):
    __tablename__ = 'user_role_associations'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True
    )
