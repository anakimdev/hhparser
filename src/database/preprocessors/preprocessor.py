import json
from abc import abstractmethod, ABC

from database.preprocessors.areas import AreaPreprocessor
from database.preprocessors.industries import IndustryPreprocessor, IndustryCategoryPreprocessor

strategies = {
    'area': AreaPreprocessor,
    'industry': IndustryPreprocessor,
    'industry_category': IndustryCategoryPreprocessor,
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