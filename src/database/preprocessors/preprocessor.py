import json
from abc import abstractmethod, ABC

from src.database.preprocessors.areas import AreaPreprocessor
from src.database.preprocessors.industries import IndustryPreprocessor, IndustryCategoryPreprocessor
from src.database.preprocessors.professions import ProfessionPreprocessor, ProfessionCategoryPreprocessor

strategies = {
    'area': AreaPreprocessor,
    'industry': IndustryPreprocessor,
    'industry_category': IndustryCategoryPreprocessor,
    'profession': ProfessionPreprocessor,
    'profession_category': ProfessionCategoryPreprocessor
}

class IPreprocessor(ABC):
    @abstractmethod
    def preprocess(self, data):
        pass


class Preprocessor():
    @staticmethod
    def preprocess(file_path:str, preprocessor:str):
        strategy = None
        if isinstance(strategies.get(preprocessor), IPreprocessor):
            strategy = strategies.get(preprocessor)

        with open(file_path, 'r') as f:
            data = json.load(f)
        return strategy.preprocess(data)