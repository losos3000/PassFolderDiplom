from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from server.configuration.basemodel import Base


class DataUserAccessOrm(Base):
    __tablename__ = "ds_data_user_access"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_data_id: Mapped[int] = mapped_column(ForeignKey("ds_data.id"))
    ds_user_id: Mapped[int] = mapped_column(ForeignKey("ds_user.id"))
    access_read: Mapped[bool] = mapped_column(default=False)
    access_edit: Mapped[bool] = mapped_column(default=False)
