import json

from src.database.preprocessors.ipreprocessor import IPreprocessor


class AreaPreprocessor(IPreprocessor):
    @staticmethod
    async def flatten_areas(areas: list, parent_id=None):
        result = []
        for area in areas:
            area_dict = {
                'api_id': int(area['id']),
                'name': area['name']
            }
            if parent_id is not None:
                area_dict['parent_id'] = int(parent_id)
            else:
                area_dict['parent_id'] = None
            result.append(area_dict)
            if area['areas']:
                result.extend(await AreaPreprocessor.flatten_areas(area['areas'], area['id']))
        return result

    @staticmethod
    async def preprocess(file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)

        result = await AreaPreprocessor.flatten_areas(data)
        return result

