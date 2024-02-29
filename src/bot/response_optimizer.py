from dataclasses import dataclass
import re


@dataclass
class Vacancy:
    name: str
    experience: str
    salary: str
    description: str
    key_skills: str
    link: str

    def __str__(self):
        return f"{self.name}\n{self.experience}\n{self.salary}\n{self.description}\n{self.key_skills}\n{self.link}"


def get_salary(item: dict[str]) -> str:
    description = f"Заработная плата:"
    if item.get('salary') is not None:
        res = item.get('salary')
        if res.get('from') is not None and res.get('to') is not None:
            return f"{description} от {res.get('from')} до {res.get('to')}"
        elif res.get('from') is not None:
            return f"{description} от {res.get('from')}"
        elif res.get('to') is not None:
            return f"{description} до {res.get('to')}"
        else:
            return f"{description} не указано"


def split_text_into_sentences(text: str) -> list[str]:
    return [sentence.lstrip('-').lstrip(' -').strip().capitalize() for sentence in text.split('.') if sentence.strip()]


def create_text(sentences: list[str]) -> str:
    r = ';\n'.join([f" - {sentence}" for sentence in sentences])
    return f'{r};'


def get_snippet(key: str, description: str, item: dict[str]) -> str:
    if item.get('snippet').get(key) is not None:
        res = create_text(split_text_into_sentences(item.get('snippet').get(key)))
        return f"\n{description} \n{res}"
    else:
        return f"\n{description} \n - Не указано"


def optimization_result(request_data: dict) -> list[str]:
    results = None

    for item in request_data.get('items'):
        if results is None:
            results = []

        name = f"Название компании: {item['employer']['name']}"
        experience = f"Требуемый опыт работы: {item['experience']['name']}"

        salary = get_salary(item)
        description = get_snippet('responsibility', 'Особенности работы:', item)
        key_skills = get_snippet('requirement', 'Ключевые навыки:', item)

        link = f"\nСсылка: {item.get('alternate_url')}"

        results.append(Vacancy(name, experience, salary, description, key_skills, link).__str__())

    return results
