from bs4 import BeautifulSoup


class Finder:
    def __init__(self, html, parser):
        self.finder = BeautifulSoup(html, parser)

    def get_elem_from_html(self, base_tag: str, attrs: dict[str] = None, searching_tag: str = None) -> str:
        if attrs is None:
            attrs = {}

        if searching_tag is None:
            searching_tag = ''

        return self.finder.find(base_tag, attrs).get(searching_tag)

    def get_list_elements(self, base_tag: str, attrs: dict[str] = None) -> list[str]:
        if attrs is None:
            attrs = {}
        return [el for el in self.finder.find_all(base_tag, attrs)]

    def get_list_by_tag(self, base_tag: str, attrs: dict[str] = None, searching_tag: str = None) -> list[str]:
        if attrs is None:
            attrs = {}
        if searching_tag is None:
            searching_tag = ''

        return self.finder.find(base_tag, attrs).find_all(searching_tag)