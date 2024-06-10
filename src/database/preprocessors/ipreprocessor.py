from abc import abstractmethod, ABC


class IPreprocessor(ABC):
    @staticmethod
    @abstractmethod
    async def preprocess(file_path:str):
        pass
