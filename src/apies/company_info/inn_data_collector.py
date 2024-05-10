from selenium import webdriver

from src.helpers.HTMLParser import HTMLParser
from src.helpers.Finder import Finder
from src.apies.company_info.configs import TYPE_HTML_PARSER, INN_URL


class InnDataCollector:
    def __init__(self):
        self.parser = None
        self.finder = None
        self.__url = None

    @property
    def url(self):
        if self.__url is not None:
            return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    async def collect_inn(self, name: str) -> str:
        data = self.normalize_inn(self.find_inn(name))
        self.parser.close_connection()
        return data

    def find_inn(self, name:str) -> str:
        key = f'{name}+инн'
        self.url = f'{INN_URL}q={key}'
        self.__get_html()

        temp = []
        spans = self.finder.get_list_by_tag('div', {'id': 'search'}, 'span')
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

    def __get_html(self):
        driver = webdriver.Chrome()
        self.parser = HTMLParser(driver)
        html = self.parser.parse_html_from_page(self.url)
        self.finder = Finder(html, TYPE_HTML_PARSER)
