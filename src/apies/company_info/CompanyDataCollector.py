from bs4 import BeautifulSoup
from src.apies.company_info.configs import HTML_PARSER


class CompanyDataCollector:
    def __init__(self):
        self.data = None

    def collect(self, html: str):
        self.get_company_from_html(html)

    @classmethod
    def get_company_from_html(cls, html: str):
        soup = BeautifulSoup(html, HTML_PARSER)
        data = [el for el in soup.find_all('div', {'class': 'pb-company-multicolumn-item'})]

        start_data = data[1:6] + data[8:12]
        middle_data = None
        if len(data) == 20:
            middle_data = data[13:17]
        elif len(data) == 23:
            middle_data = data[13:18]

        temp_data = start_data + middle_data
        names = cls.normalize_data('div', {'class': 'pb-company-field-name'}, temp_data)
        values = cls.normalize_data('div', {'class': 'pb-company-field-value'}, temp_data, True)
        return list(zip(names, values))

    @classmethod
    def normalize_data(cls, tag: str, attrs: dict[str, str], data: list[str], is_values: bool = False) -> list[str]:
        if is_values:
            return list(map(lambda x: ' '.join(x.find(tag, attrs).text.strip().split()), data))
        else:
            return list(map(lambda x: x.find(tag, attrs).text.strip().replace(':', ''), data))
