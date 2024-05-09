from pprint import pprint
from dataclasses import dataclass


@dataclass
class Company:
    data: list[tuple[str, str]]
    list_of_strings: list[str] = None

    def get_list_of_strings(self) -> list[str]:
        if self.list_of_strings is None:
            self.list_of_strings = []

            for item in self.data:
                string = f'{item[0]}: {item[1]}'
                self.list_of_strings.append(string)

        return self.list_of_strings


def make_desc_company(data: list[tuple[str, str]]) -> list[str]:
    list_of_strings = None
    if list_of_strings is None:
        list_of_strings = []

    for item in data:
        string = f'{item[0]}: {item[1]}'
        list_of_strings.append(string)

    return list_of_strings


if __name__ == "__main__":
    tinkoff_data = [('Полное наименование', 'АКЦИОНЕРНОЕ ОБЩЕСТВО "ТИНЬКОФФ БАНК"'),
                    ('Сокращенное наименование', 'АО "ТИНЬКОФФ БАНК"'),
                    ('ОГРН', '1027739642281'), ('Дата регистрации', '28.01.1994'),
                    ('Способ образования', 'Создание юридического лица до 01.07.2002'),
                    ('ИНН', '7710140679'), ('Дата постановки на учёт', '18.03.2021'),
                    ('Наименование налогового органа', 'Инспекция Федеральной налоговой службы № 13 по г.Москве'),
                    ('КПП', '771301001'),
                    ('Основной вид деятельности (ОКВЭД)', '64.19 Денежное посредничество прочее'),
                    ('Адрес организации',
                     '127287, Г.МОСКВА, ВН.ТЕР.Г. МУНИЦИПАЛЬНЫЙ ОКРУГ САВЕЛОВСКИЙ, УЛ ХУТОРСКАЯ 2-Я, Д. 38А, СТР. 26'),
                    ('Сведения об уставном капитале (складочном капитале, уставном фонде, паевых взносах)',
                     '6 772 000 000 ₽ (УСТАВНЫЙ КАПИТАЛ)'),
                    ('Сведения о субъекте МСП', 'Не является субъектом МСП')]

