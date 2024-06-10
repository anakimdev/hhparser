import asyncio
import json

from src.database.preprocessors.ipreprocessor import IPreprocessor


class IndustryCategoryPreprocessor(IPreprocessor):
    @staticmethod
    async def preprocess(file_path:str):
        with open(file_path, 'r') as f:
            data = json.load(f)
        categories = [el['name'] for el in data]
        return categories


class IndustryPreprocessor(IPreprocessor):
    @staticmethod
    async def preprocess(file_path:str):
        with open(file_path, 'r') as f:
            data = json.load(f)

        industries = []
        links = {}
        idx = 1

        for category in data:
            links[category['id']] = idx
            idx += 1

        tasks = []
        for category in data:
            for industry in category['industries']:
                task = asyncio.create_task(IndustryPreprocessor._process_industry(industry, links))
                tasks.append(task)

        results = await asyncio.gather(*tasks)
        industries.extend(results)
        return industries

    @staticmethod
    async def _process_industry(industry:dict[str], links:dict):
        return {
            'name': industry['name'],
            'category_id': links[industry['id'].split('.')[0]]
        }