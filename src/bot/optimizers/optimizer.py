from src.apies.company_info.configs import INN_URL
from src.apies.main import create_hunter_collector, create_company_collector, create_inn_collector
from src.bot.optimizers.company_optimizer import Company, make_desc_company
from src.bot.optimizers.vacancy_optimizer import make_desc_vacancies, make_desc_vacancy, Vacancy, VacancyDesc

hh_collector = create_hunter_collector()
inn_collector = create_inn_collector()
company_collector = create_company_collector()


async def get_vacancies(request_data: dict[str]) -> list[Vacancy]:
    return make_desc_vacancies(await hh_collector.collect_vacancies(request_data))


async def get_vacancy(vacancy_id: str) -> VacancyDesc:
    return make_desc_vacancy(await hh_collector.collect_vacancy(vacancy_id))


async def get_areas(data: dict[str]):
    return await hh_collector.collect_areas(data)


def get_company_info(name: str) -> list[str]:
    inn = inn_collector.collect_inn(name)
    company = company_collector.collect_company_data(inn)
    return make_desc_company(company)

