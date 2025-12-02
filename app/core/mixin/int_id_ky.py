from sqlalchemy.orm import mapped_column, Mapped

class IntIdPk:
    __abstract__ = True   

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
