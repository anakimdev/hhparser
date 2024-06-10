import asyncio
import itertools
import json
import os

from src.database.preprocessors.ipreprocessor import IPreprocessor


class VacancyPreprocessor(IPreprocessor):
    @staticmethod
    async def preprocess(file_path: str):
        common_list = []
        tasks = []

        for file in os.listdir(file_path):
            task = asyncio.create_task(
                VacancyPreprocessor.__add_to_common_list
                (common_list, VacancyPreprocessor._process_file, file_path + file)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
        return common_list


    @staticmethod
    async def _process_file(path: str):
        with open(f'{path}', 'r') as f:
            data = json.load(f)
            data = [
                {
                    **vacancy,
                    'api_id': int(vacancy['api_id']),
                    'area_id': int(vacancy['area_id']),
                    'professional_roles': [
                        {**role, 'id': int(role['id'])} for role in vacancy['professional_roles']
                    ]
                } for vacancy in data
            ]
            return data

    @staticmethod
    async def __add_to_common_list(common_list, task_func, *args, **kwargs):
        result = await task_func(*args, **kwargs)
        common_list.extend(result)

