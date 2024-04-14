from src.apies.Response import Response


class HHDataCollector:
    def __init__(self, token: str, useragent: str, base_url: str):
        self.__token = token
        self.__useragent = useragent
        self.__base_url = base_url

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

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, new_url: str):
        self.__base_url = new_url

    def __get_headers(self) -> dict[str]:
        return {'Authorization': f'Bearer {self.token}', 'User-Agent': self.useragent}

    async def collect_vacancies(self, data):
        return Response.get_response(url = f'{self.base_url}/vacancies', data = data, headers = self.__get_headers())

    async def collect_vacancy(self, vacancy_id: str):
        return Response.get_response(url = f'{self.base_url}/vacancies/{vacancy_id}', headers = self.__get_headers())

    async def collect_areas(self, data: dict[str]):
        return Response.get_response_by_chunk(url = f'{self.base_url}/areas', filename = 'areas', data = data,
            headers = self.__get_headers())
