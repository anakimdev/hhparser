import asyncio

from src.apies.main import create_hunter_collector, create_company_collector, create_inn_collector
from src.bot.optimizers.company_optimizer import make_desc_company
from src.bot.optimizers.vacancy_optimizer import make_desc_vacancies, make_desc_vacancy, Vacancy, VacancyDesc

hh_collector = create_hunter_collector()
inn_collector = create_inn_collector()
company_collector = create_company_collector()


async def get_vacancy(vacancy_id: str) -> VacancyDesc:
    return make_desc_vacancy(await hh_collector.collect_vacancy(vacancy_id))


async def get_vacancies(request_data: dict[str]) -> list[Vacancy]:
    vacancies_data = await hh_collector.collect_vacancies(request_data)

    ids = []
    ids.extend(x["id"] for x in vacancies_data["items"])

    responsibilities = []
    responsibilities.extend(x["snippet"]['responsibility'] for x in vacancies_data["items"])

    vacancies = []
    for vacancy_id in ids:
        vacancies.append(await hh_collector.collect_vacancy(vacancy_id))

    for index, vacancy in enumerate(vacancies):
        vacancy['responsibility'] = responsibilities[index]

    result = make_desc_vacancies(vacancies)
    return result


async def get_areas(data: dict[str]):
    return hh_collector.collect_areas(data)


async def get_company_info(name: str) -> dict[str, list[str]]:
    inn = await inn_collector.collect_inn(name)
    company = await company_collector.collect_company_data(inn)
    return make_desc_company(company)


async def get_vacancy_statistics(name: str):
    vacancies = hh_collector.collect_vacancies({'text': name})
    return vacancies
