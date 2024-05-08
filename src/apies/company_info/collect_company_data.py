from bs4 import BeautifulSoup
from selenium import webdriver
import time

from src.apies.company_info.configs import INN_URL, FNS_URL, HTML_PARSER, FNS_SEARCH_URL
from src.apies.company_info.InnDataCollector import InnDataCollector
from src.apies.company_info.CompanyDataCollector import CompanyDataCollector


def get_html_from_page(requester: webdriver, url: str) -> str:
    requester.get(url)
    time.sleep(5)
    return requester.page_source


def get_inn(handler: webdriver, url: str) -> str:
    html = get_html_from_page(handler, url=url)
    return InnDataCollector.normalize_inn(InnDataCollector.find_inn(html))


def get_attr(html: str) -> str:
    soup = BeautifulSoup(html, HTML_PARSER)
    link = soup.find('div', {'class': 'pb-card'}).get('data-href')
    return link


def parse_html_from_page(handler: webdriver, number_inn: str):
    link_html = get_html_from_page(handler, url=f'{FNS_SEARCH_URL}queryAll={number_inn}')
    attr = get_attr(link_html)
    company_html = get_html_from_page(handler, url=f'{FNS_URL}{attr}')
    return company_html


def get_company_data(handler: webdriver, number_inn: str):
    cc = CompanyDataCollector()
    cc.collect(parse_html_from_page(handler, number_inn))


if __name__ == '__main__':
    driver = webdriver.Chrome()
    key = 'сбербанк' + "+" + 'инн'
    try:
        inn = get_inn(driver, f'{INN_URL}q={key}')
        get_company_data(driver, inn)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
