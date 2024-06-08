import json

from src.database.core.engine import async_session
from src.database.models.common_dicts import IndustryCategoriesTable, IndustriesTable
from src.database.preprocessors.preprocessor import Preprocessor
from src.database.preprocessors.configs import INDUSTRY_FILE


class IndustryOrm:
    @staticmethod
    async def insert_industry_categories():
        categories = [IndustryCategoriesTable(name=category) for category in
                      Preprocessor.preprocess(INDUSTRY_FILE, 'industry_category')]

        async with async_session() as session:
            session.add_all(categories)
            await session.commit()

    @staticmethod
    async def insert_industries():
        async with async_session() as session:
            data = Preprocessor.preprocess(INDUSTRY_FILE, 'industry')
            industries = []

            for industry in data:
                industries.append(IndustriesTable(name=industry['name'], category_id=industry['category_id']))

            session.add_all(industries)
            await session.commit()


