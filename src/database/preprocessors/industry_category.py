import json


def preprocess_industry_categories():
    categories = []

    with open('data/industries.json', 'r') as f:
        data = json.load(f)

    for category in data:
        categories.append(category['name'])

    return categories