from selenium import webdriver

from src.helpers.HTMLParser import HTMLParser
from src.helpers.Finder import Finder
from src.apies.company_info.configs import TYPE_HTML_PARSER, INN_URL

driver = webdriver.Chrome()
parser = HTMLParser(driver)


class InnDataCollector:
    def __init__(self, url: str):
        self.parser = parser
        self.finder = None
        self.url = url

    def collect_inn(self) -> str:
        return self.normalize_inn(self.find_inn())

    def find_inn(self) -> str:
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
        html = self.parser.parse_html_from_page(self.url)
        self.finder = Finder(html, TYPE_HTML_PARSER)
