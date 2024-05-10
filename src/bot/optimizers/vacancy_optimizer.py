from dataclasses import dataclass

from src.bot.optimizers.text_optimizer import make_description, make_key_skills, make_responsibility


@dataclass
class VacancyDesc:
    name: str
    description: str
    link: str

    def __str__(self):
        return self.description

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
        return f'{self.name}\n{self.experience}\n{self.salary}\n\n{self.description}\n\n{self.key_skills}'

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


def get_key_skills(data: list[dict[str]]) -> str:
    if not data:
        return f'Ключевые навыки: не указано'

    skills =  make_key_skills(data)
    key_skills = ';\n- '.join(skills)
    return f'Ключевые навыки:\n- {key_skills};'


def get_description(description: str) -> str:
    if not description:
        return 'Описания нет'

    return make_description(description)


def get_responsibility(description: str) -> str:
    if description is None:
        return f'Обязанности: не указано'

    my_strings = make_responsibility(description)
    string = ';\n- '.join(my_strings)
    return f'Обязанности: \n- {string};'


def make_desc_vacancies(vacancies: list[dict[str]]) -> list[Vacancy]:
    results = None
    for vacancy in vacancies:
        if results is None:
            results = []

        name = f"Компания: {vacancy['employer']['name']}"
        experience = f"Требуемый опыт работы: {vacancy['experience']['name']}"
        salary = get_salary(vacancy)
        description = get_responsibility(vacancy['responsibility'])
        key_skills = get_key_skills(vacancy['key_skills'])
        link = vacancy['alternate_url']

        results.append(Vacancy(name=name, experience=experience, salary=salary, description=description,
                               key_skills=key_skills, link=link))

    return results


def make_desc_vacancy(response_data: dict[str]) -> VacancyDesc:
    name = f"Компания: {response_data['employer']['name']}"
    description = get_description(response_data.get('description'))
    link = response_data.get('alternate_url')
    return VacancyDesc(name=name, description=description, link=link)
