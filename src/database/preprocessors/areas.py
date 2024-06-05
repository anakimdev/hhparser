import json

def preprocess_areas():
    def flatten_areas(areas:list, parent_id=None):
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
                result.extend(flatten_areas(area['areas'], area['id']))
        return result

    with open('data/areas.json', 'r') as f:
        data = json.load(f)

    result = flatten_areas(data)

    return result
