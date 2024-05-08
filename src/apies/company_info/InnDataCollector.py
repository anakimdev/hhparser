from dataclasses import dataclass
from bs4 import BeautifulSoup

from src.apies.company_info.configs import HTML_PARSER


@dataclass
class InnDataCollector:
    @classmethod
    def find_inn(cls, html: str) -> str:
        soup = BeautifulSoup(html, HTML_PARSER)
        temp = []
        spans = soup.find('div', id='search').find_all('span')

        for item in spans:
            text = item.get_text()
            index = text.find('ИНН')
            if index != -1:
                temp.append(text[index:index + 15])

        if len(temp) > 0:
            return temp[0]

    @staticmethod
    def normalize_inn(string_inn: str) -> str:
        numbers = '0123456789'
        if string_inn != '':
            return ''.join([char for char in string_inn if char in numbers])
