from sqlalchemy import select

from server.configuration.database import session_factory
from server.role.models import RoleOrm
from server.role.schemas import SRoleAdd


class RoleManager:
    @classmethod
    async def add_role(cls, data: SRoleAdd) -> int:
        async with session_factory() as session:
            role_dict = data.model_dump()
            role = RoleOrm(**role_dict)
            session.add(role)
            await session.flush()
            await session.commit()
            return role.id

    @classmethod
    async def read_role_all(cls):
        async with session_factory() as session:
            query = select(RoleOrm)
            result = await session.execute(query)
            role_model = result.scalars().all()
            return role_model
