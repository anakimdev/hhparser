import json

from src.database.core.engine import async_session
from src.database.models.dictionaries import WorkloadTable, IndustryCategoryTable, IndustryTable
from src.database.preprocessors.industries import preprocess_industries
from src.database.preprocessors.industry_category import preprocess_industry_categories


class IndustryOrm:
    @staticmethod
    async def insert_industry_categories():
        categories = [IndustryCategoryTable(name=category) for category in preprocess_industry_categories()]

        async with async_session() as session:
            session.add_all(categories)
            await session.commit()

    @staticmethod
    async def insert_industries():
        async with async_session() as session:
            data = preprocess_industries()
            industries = []

            for industry in data:
                industries.append(IndustryTable(name=industry['name'], category_id=industry['category_id']))

            session.add_all(industries)
            await session.commit()


