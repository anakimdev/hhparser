from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.preprocessors.preprocessor import Preprocessor
from src.database.preprocessors.configs import AREAS_FILE
from src.database.core.engine import async_session
from src.database.models.common_dicts import AreasTable


class AreaOrm:

    @staticmethod
    async def insert_areas():
        async with async_session() as session:
            areas = []
            data = await Preprocessor.preprocess(AREAS_FILE, 'area')
            for area in data:
                if area['parent_id']:
                    areas.append(AreasTable(parent_id=area['parent_id'], name=area['name'], api_id=area['api_id']))
                else:
                    areas.append(AreasTable(name=area['name'], api_id=area['api_id']))

            session.add_all(areas)
            await session.commit()

    @staticmethod
    async def select_area_by_name(name:str):
        async with async_session() as session:
            query = (
                select(AreasTable)
                .options(joinedload(AreasTable.parent).load_only(AreasTable.name))
                .filter_by(name=name)
            )
            res = await session.execute(query)
            result = res.scalars().first()
            return result