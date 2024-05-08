import requests
from typing import Union


class Response:
    @staticmethod
    def get_response(url: str, data: Union[dict, None] = None, headers: Union[dict, None] = None) -> str:
        response = requests.get(url = url, data = data, headers = headers)
        return response.json()

    @staticmethod
    def get_response_by_chunk(url: str, filename:str, data: Union[dict, None] = None, headers: Union[dict, None] = None):
        chunk_size = 1024
        with requests.get(url = url, data =data, headers = headers, stream = True) as r:
            with open(f'src/data/{filename}.json', 'wb') as f:
                for chunk in r.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)


