import time


class HTMLParser:
    def __init__(self, driver):
        self.webdriver = driver

    def parse_html_from_page(self, url: str) -> str:
        return self.__get_html_from_page(url)

    def __get_html_from_page(self, url: str) -> str:
        self.webdriver.get(url)
        time.sleep(5)
        return self.webdriver.page_source
