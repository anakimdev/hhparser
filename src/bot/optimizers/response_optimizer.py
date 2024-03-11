from dataclasses import dataclass
from pprint import pprint

from markdown import markdown
from markdownify import markdownify as md


@dataclass
class VacancyDesc:
    name: str
    description: str
    link: str

    def __str__(self):
        return md(markdown(f"{self.description}"), heading_style = "")

    def get_link(self):
        return self.link

    def get_name(self):
        return self.name


@dataclass
class Vacancy(VacancyDesc):
    experience: str
    salary: str
    key_skills: str

    def __str__(self):
        return md(markdown(f"{self.name}\n{self.experience}\n{self.salary}\n\n{self.description}\n\n{self.key_skills}"))


def get_salary(item: dict[str]) -> str:
    description = f"Заработная плата:"
    if item.get('salary') is None:
        return f"{description} не указано"

    res = item.get('salary')
    if res.get('from') is not None and res.get('to') is not None:
        return f"{description} от {res.get('from')} до {res.get('to')}"
    elif res.get('from') is not None:
        return f"{description} от {res.get('from')}"
    elif res.get('to') is not None:
        return f"{description} до {res.get('to')}"


def split_text_into_sentences(text: str) -> list[str]:
    return [sentence.lstrip('-').lstrip(' -').strip().capitalize() for sentence in text.split('.') if sentence.strip()]


def create_text(sentences: list[str]) -> str:
    r = ';\n'.join([f" - {sentence}" for sentence in sentences])
    return f'{r};'


def get_snippet(key: str, description: str, item: dict[str]) -> str:
    if item.get('snippet').get(key) is not None:
        res = create_text(split_text_into_sentences(item.get('snippet').get(key)))
        return f"{description}\n{res}"
    else:
        return f"{description}\n - Не указано"


def make_desc_vacancies(response_data: dict) -> list[Vacancy]:
    results = None

    for item in response_data.get('items'):
        if results is None:
            results = []

        name = f"Компания: {item['employer']['name']}"
        experience = f"Требуемый опыт работы: {item['experience']['name']}"
        salary = get_salary(item)
        description = get_snippet('responsibility', 'Особенности работы:', item)
        key_skills = get_snippet('requirement', 'Ключевые навыки:', item)
        link = item.get('alternate_url')

        results.append(Vacancy(name = name, experience = experience, salary = salary, description = description,
            key_skills = key_skills, link = link))

    return results


def make_desc_vacancy(response_data: dict[str]) -> VacancyDesc:
    name = f"Компания: {response_data['employer']['name']}"
    description = response_data.get('description')
    link = response_data.get('alternate_url')
    return VacancyDesc(name = name, description = description, link = link)
