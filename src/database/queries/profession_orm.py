import asyncio
from asyncio import create_task

from sqlalchemy import Executable, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from src.database.core.engine import async_session
from src.database.models.profession_models.professions import ProfessionsTable
from src.database.models.profession_models.profession_categories import ProfessionCategoriesTable
from src.database.preprocessors.configs import PROFESSIONS_FILE
from src.database.preprocessors.preprocessor import Preprocessor


class ProfessionOrm:
    @staticmethod
    async def insert_categories():
        prepare_data = await Preprocessor.preprocess(PROFESSIONS_FILE, 'profession_category')
        categories = [ProfessionCategoriesTable(name=category['name'], api_id=category['api_id']) for category in
                      prepare_data]

        async with async_session() as session:
            session.add_all(categories)
            await session.commit()

    @staticmethod
    async def get_category_by_api_id(api_id: int, session: AsyncSession | None = None):
        query = (
            select(ProfessionCategoriesTable)
            .options(selectinload(ProfessionCategoriesTable.professions))
            .filter_by(api_id=api_id)
        )

        res = await ProfessionOrm.__get_one(query, session)
        return res

    @staticmethod
    async def get_all_categories_by_api_ids(api_ids: list[int], session: AsyncSession | None = None):
        query = (
            select(ProfessionCategoriesTable)
            .filter(ProfessionCategoriesTable.api_id.in_(api_ids))
        )

        res = await session.scalars(query)
        return res.all()

    @staticmethod
    async def insert_professions():
        async with async_session() as session:
            prepare_data = await Preprocessor.preprocess(PROFESSIONS_FILE, 'profession')
            tasks = []
            for profession in prepare_data:
                task = create_task(ProfessionOrm._insert_profession(profession, session))
                tasks.append(task)
            professions = await asyncio.gather(*tasks)

            session.add_all(professions)
            await session.commit()

    @staticmethod
    async def _insert_profession(profession, session: AsyncSession):
        profession_obj = ProfessionsTable(
            api_id=profession['api_id'],
            name=profession['name'],
        )

        category_api_ids = [category['id'] for category in profession['categories']]
        categories = await ProfessionOrm.get_all_categories_by_api_ids(category_api_ids, session)
        profession_obj.categories = categories

        return profession_obj

    @staticmethod
    async def get_profession_by_api_id(api_id: int, session: AsyncSession|None = None):
        query = (
            select(ProfessionsTable)
            .options(selectinload(ProfessionsTable.categories))
            .filter_by(api_id=api_id)
        )

        res = await ProfessionOrm.__get_one(query, session)
        return res

    @staticmethod
    async def __get_one(query: Executable, session: AsyncSession|None = None):
        if session:
            res = await session.execute(query)
            result = res.scalars().first()
            return result
        else:
            async with async_session() as session:
                res = await session.execute(query)
                result = res.scalars().first()
                return result

