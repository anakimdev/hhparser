import asyncio
import json


from src.database.preprocessors.ipreprocessor import IPreprocessor


class ProfessionCategoryPreprocessor(IPreprocessor):
    @staticmethod
    async def preprocess(file_path:str):
        with open(file_path, 'r') as f:
            data = json.load(f)

        tasks = []
        for category in data['categories']:
            task = asyncio.create_task(ProfessionCategoryPreprocessor._process_category(category))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    async def _process_category(category: dict[str]):
        return {"api_id": int(category['id']), "name": category['name']}


class ProfessionPreprocessor(IPreprocessor):
    @staticmethod
    async def preprocess(file_path:str):
        with open(file_path, 'r') as f:
            data = json.load(f)

        tasks = []
        for category in data['categories']:
            parent_id = category['id']
            for item in category['roles']:
                task = asyncio.create_task(ProfessionPreprocessor._process_profession(item, parent_id))
                tasks.append(task)

        results = await asyncio.gather(*tasks)
        res = sorted(results, key=lambda x: x['api_id'])
        i = 0
        while i < len(res) - 1:
            if res[i]['api_id'] == res[i+1]['api_id']:
                res[i]['categories'].extend(res[i+1]['categories'])
                res.pop(i+1)
            else:
                i += 1
        return res

    @staticmethod
    async def _process_profession(profession, parent_id):
        return {"name": profession['name'], "api_id": int(profession['id']), "categories": [{"id": int(parent_id)}]}
