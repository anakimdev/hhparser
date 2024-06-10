import asyncio
from pprint import pprint

from src.database.preprocessors.areas import AreaPreprocessor
from src.database.preprocessors.configs import PROFESSIONS_FILE, VACANCIES_FILE
from src.database.preprocessors.industries import IndustryPreprocessor, IndustryCategoryPreprocessor
from src.database.preprocessors.ipreprocessor import IPreprocessor
from src.database.preprocessors.professions import ProfessionPreprocessor, ProfessionCategoryPreprocessor
from src.database.preprocessors.vacancies import VacancyPreprocessor

strategies = {
    'area': AreaPreprocessor,
    'industry': IndustryPreprocessor,
    'industry_category': IndustryCategoryPreprocessor,
    'profession': ProfessionPreprocessor,
    'profession_category': ProfessionCategoryPreprocessor,
    'vacancy': VacancyPreprocessor
}


class Preprocessor:
    @staticmethod
    async def preprocess(file_path: str, preprocessor: str):
        strategy = None
        if issubclass(strategies.get(preprocessor), IPreprocessor):
            strategy = strategies.get(preprocessor)
        else:
            raise ValueError('Unknown preprocessor')

        result = await strategy.preprocess(file_path)
        return result

