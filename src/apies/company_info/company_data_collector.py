from selenium import webdriver

from src.apies.company_info.configs import TYPE_HTML_PARSER, FNS_URL, FNS_SEARCH_URL
from src.helpers.Finder import Finder
from src.helpers.HTMLParser import HTMLParser


class CompanyDataCollector:
    def __init__(self):
        self.finder = None
        self.data = None
        self.parser = None
        self.inn = None

    async def collect_company_data(self, inn: str) -> list[tuple[str, str]]:
        data = self.get_company_from_html(inn)
        self.parser.close_connection()
        return data

    def get_company_from_html(self, inn: str) -> list[tuple[str, str]]:
        self.inn = inn
        html = self.__get_company_html()
        self.finder = Finder(html, TYPE_HTML_PARSER)
        data = self.finder.get_list_elements('div', {'class': 'pb-company-multicolumn-item'})

        start_data = data[1:6] + data[8:12]
        middle_data = None
        if len(data) in range(20, 23):
            middle_data = data[13:17]
        elif len(data) >= 23:
            middle_data = data[13:18]

        temp_data = start_data + middle_data
        names = self.normalize_data('div', {'class': 'pb-company-field-name'}, temp_data)
        values = self.normalize_data('div', {'class': 'pb-company-field-value'}, temp_data, True)
        return list(zip(names, values))

    @staticmethod
    def normalize_data(tag: str, attrs: dict[str, str], data: list[str], is_values: bool = False) -> list[str]:
        if is_values:
            return list(map(lambda x: ' '.join(x.find(tag, attrs).text.strip().split()), data))
        else:
            return list(map(lambda x: x.find(tag, attrs).text.strip().replace(':', ''), data))

    def __get_company_html(self):
        driver = webdriver.Chrome()
        self.parser = HTMLParser(driver)
        temp_fns = self.parser.parse_html_from_page(url=f'{FNS_SEARCH_URL}queryAll={self.inn}')
        self.finder = Finder(temp_fns, TYPE_HTML_PARSER)
        attr = self.finder.get_elem_from_html('div', {'class': 'pb-card'}, 'data-href')
        return self.parser.parse_html_from_page(url=f'{FNS_URL}{attr}')
