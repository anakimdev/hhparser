from src.bot.optimizers.text_optimizer import make_description, make_key_skills, make_responsibility, make_salary
from src.bot.models.vacancy_desc import VacancyDesc
from src.bot.models.vacancy import Vacancy


def get_salary(item: dict) -> str:
    return make_salary(item)


def get_key_skills(data: list[dict[str]]) -> str:
    if not data:
        return f'Ключевые навыки: не указано'

    skills =  make_key_skills(data)[:5]
    key_skills = ';\n- '.join(skills)
    return f'Ключевые навыки:\n- {key_skills};'


def get_description(description: str) -> str:
    if not description:
        return 'Описания нет'

    return make_description(description)


def get_responsibility(description: str) -> str:
    if description is None:
        return f'Обязанности: не указано'

    my_strings = make_responsibility(description)[:5]
    string = ';\n- '.join(my_strings)
    return f'Обязанности: \n- {string};'


def make_desc_vacancies(vacancies: list[dict[str]]) -> list[Vacancy]:
    results = None
    for vacancy in vacancies:
        if results is None:
            results = []

        company_name = f"Компания: {vacancy['employer']['name']}"
        experience = f"Требуемый опыт работы: {vacancy['experience']['name']}"
        salary = get_salary(vacancy)
        description = get_responsibility(vacancy['responsibility'])
        key_skills = get_key_skills(vacancy['key_skills'])
        link = vacancy['alternate_url']

        results.append(Vacancy(company_name, description, link, experience, salary,
                               key_skills))

    return results


def make_desc_vacancy(response_data: dict[str]) -> VacancyDesc:
    company_name = f"Компания: {response_data['employer']['name']}"
    description = get_description(response_data.get('description'))
    link = response_data.get('alternate_url')
    return VacancyDesc(company_name, description, link)
