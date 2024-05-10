


# from typing import Optional
#
# from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
# from sqlalchemy import Integer, ForeignKey
#
# from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
#
#
# class UserOrm(SQLAlchemyBaseUserTable[int], Base):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     login: Mapped[str]
#     role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"))
#     pass
#
#
# class RoleOrm(Base):
#     __tablename__ = "role"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     description: Mapped[Optional[str]]
