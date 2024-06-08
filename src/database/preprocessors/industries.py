from database.preprocessors.preprocessor import IPreprocessor


class IndustryCategoryPreprocessor(IPreprocessor):
    def preprocess(self, data):
        categories = [el['name'] for el in data]
        return categories


class IndustryPreprocessor(IPreprocessor):
    def preprocess(self, data):
        industries = []
        links = {}
        idx = 1

        for category in data:
            links[category['id']] = idx
            idx += 1

        for category in data:
            for industry in category['industries']:
                industries.append({
                    'name': industry['name'],
                    'category_id': links[industry['id'].split('.')[0]]
                })
        return industries
