from pprint import pprint

from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from dataclasses import dataclass
import time

from src.apies.company_info.configs import INN_URL, FNS_URL, HTML_PARSER, FNS_SEARCH_URL

driver = webdriver.Chrome()
key = 'сбербанк' + "+" + 'инн'
inns = []


def get_html_from_page(requester: webdriver, url: str) -> str:
    requester.get(url)
    time.sleep(5)
    return requester.page_source


@dataclass
class InnParser:
    html: str
    inn: str = ''

    def get_inn(self) -> str:
        self.__find_inn()
        self.__normalize_inn()
        return self.inn

    def __find_inn(self):
        soup = BeautifulSoup(self.html, HTML_PARSER)
        temp = []
        spans = soup.find('div', id='search').find_all('span')

        for item in spans:
            text = item.get_text()
            index = text.find('ИНН')
            if index != -1:
                temp.append(text[index:index + 15])

        if len(temp) > 0:
            self.string_inn = temp[0]

    def __normalize_inn(self):
        numbers = '0123456789'
        if self.string_inn != '':
            self.inn = ''.join([char for char in self.string_inn if char in numbers])


@dataclass
class CompanyInfoParser:
    pass


def get_inn(handler: webdriver, url: str) -> str:
    html = get_html_from_page(handler, url=url)
    parser = InnParser(html=html)
    return parser.get_inn()


def get_attr(html: str) -> str:
    soup = BeautifulSoup(html, HTML_PARSER)
    link = soup.find('div', {'class': 'pb-card'}).get('data-href')
    return link


def parse_html_from_page(handler: webdriver, inn: str):
    link_html = get_html_from_page(handler, url=f'{FNS_SEARCH_URL}queryAll={inn}')
    attr = get_attr(link_html)
    company_html = get_html_from_page(handler, url = f'{FNS_URL}{attr}')
    return company_html


def optimize_data(keys: list[str], values: list[str]):
    pass


def get_data_from_txt():
    with open('test/index.html', 'r') as fp:
        soup = BeautifulSoup(fp, HTML_PARSER)
        data = [el for el in soup.find_all('div', {'class': 'pb-company-multicolumn-item'})]

        start_data = data[1:7] + data[8:12]
        if len(data) == 20:
            middle_data = data[13:17]
        elif len(data) == 23:
            middle_data = data[13:18]

        charset_normalizer = {'\n': ''}
        start_names = list(map(lambda x: x.find('div', {'class': 'pb-company-field-name'}).text.strip(), start_data))
        start_values = list(map(lambda x: x.find('div', {'class': 'pb-company-field-value'}).text.strip(), start_data))
        middle_names = list(map(lambda x: ' '.join(x.find('div', {'class': 'pb-company-field-name'}).text.split()), middle_data))
        middle_values = list(map(lambda x: ' '.join(x.find('div', {'class': 'pb-company-field-value'}).text.split()), middle_data))
        for key, value in zip(middle_names, middle_values):
            print(f'{key} {value}')


def get_data_from_html(html: str):
    soup = BeautifulSoup(html, HTML_PARSER)


def get_company_data(handler: webdriver, inn: str):
    get_data_from_txt()
    # get_data_from_html(parse_html_from_page(handler, inn))


try:
    inn = get_inn(driver, f'{INN_URL}q={key}')
    get_company_data(driver, inn)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
