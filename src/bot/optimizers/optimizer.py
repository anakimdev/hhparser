from src.apies.main import create_data_collector
from src.bot.optimizers.vacancy_optimizer import make_desc_vacancies, make_desc_vacancy, Vacancy, VacancyDesc

collector = create_data_collector()


async def get_vacancies(request_data: dict[str]) -> list[Vacancy]:
    return make_desc_vacancies(await collector.collect_vacancies(request_data))


async def get_vacancy(vacancy_id: str) -> VacancyDesc:
    return make_desc_vacancy(await collector.collect_vacancy(vacancy_id))


async def get_areas(data: dict[str]):
    return await collector.collect_areas(data)

