import json


def preprocess_industries():
    industries = []
    links = {}
    idx = 1

    with open('data/industries.json', 'r') as f:
        data = json.load(f)

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

