from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from database.core.engine import async_session
from database.models.dictionaries import AreaTable
from database.preprocessors.areas import preprocess_areas


class AreaOrm():
    @staticmethod
    async def insert_areas():
        async with async_session() as session:
            areas = []
            data = preprocess_areas()
            for area in data:
                if area['parent_id']:
                    areas.append(AreaTable(parent_id=area['parent_id'], name=area['name'], api_id=area['api_id']))
                else:
                    areas.append(AreaTable(name=area['name'], api_id=area['api_id']))

            session.add_all(areas)
            await session.commit()

    @staticmethod
    async def select_area_by_name(name:str):
        async with async_session() as session:
            query = (
                select(AreaTable)
                .options(joinedload(AreaTable.parent).load_only(AreaTable.name))
                .filter_by(name=name)
            )
            res = await session.execute(query)
            result = res.scalars().first()
            return result