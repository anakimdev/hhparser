from src.database.preprocessors.preprocessor import IPreprocessor


class ProfessionCategoryPreprocessor(IPreprocessor):
    def preprocess(self, data):
        categories = []

        for category in data:
            categories.append({"name": category['name'], "api_id": category['id']})

        return categories


class ProfessionPreprocessor(IPreprocessor):
    def preprocess(self, data):
        professions = []

        for category in data:
            parent_id = category['id']
            for item in category['roles']:
                professions.append({"name": item['name'], "api_id": item['id'], "parent_id":parent_id})

        return professions
