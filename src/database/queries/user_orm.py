from sqlalchemy import select

from src.database.core.engine import async_session
from src.database.models.users import UsersTable, UserTemplatesTable
from src.database.schemas_dto.user_dto import UsersTemplatesDTO, UsersAddDTO, UsersTemplatesAddDTO, UsersDTO


class UserOrm:
    @staticmethod
    async def insert_user(user_dto: UsersAddDTO):
        async with async_session() as session:
            session.add(UsersTable(nickname=user_dto.nickname, telegram_id=user_dto.telegram_id))
            await session.commit()


    @staticmethod
    async def get_user_by_telegram_id(telegram_id: int):
        async with async_session() as session:
            query = (
                select(UsersTable)
                .filter_by(telegram_id=telegram_id)
            )

            res = session.execute(query)
            result = res.scalars().first()
            res_dto = UsersDTO.model_validate(result, from_attributes=True)
            return res_dto

    @staticmethod
    async def insert_user_template(user_template: UsersTemplatesAddDTO):
        async with async_session() as session:
            session.add(UserTemplatesTable(user_id=user_template.user_id, profession=user_template.profession,
                                           expected_salary=user_template.expected_salary, region=user_template.region))
            await session.commit()

    @staticmethod
    async def get_user_templates(user_id: int):
        async with async_session() as session:
            query = (
                select(UserTemplatesTable)
                .filter_by(user_id=user_id)
            )
            res = await session.execute(query)
            results = res.scalars().all()
            results_dto = [UsersTemplatesDTO.model_validate(row, from_attributes=True) for row in results]
            return results_dto