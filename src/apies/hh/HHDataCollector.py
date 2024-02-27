from pprint import pprint

import requests

class HHDataCollector:
    def __init__(self, token:str, useragent:str):
        self.__token = token
        self.__useragent = useragent

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token: str):
        self.__token = token

    @property
    def useragent(self):
        return self.__useragent

    @useragent.setter
    def useragent(self, new_agent: str):
            self.__useragent = new_agent

    def get_vacancies(self, data):
        url = 'https://api.hh.ru/vacancies'
        data = data
        headers = {'Authorization': f'Bearer {self.token}',
                    'User-Agent': self.useragent}
        response = requests.get(url = url, data = data, headers = headers)
        return response.json()

