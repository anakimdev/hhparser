from dataclasses import dataclass

from src.bot.models.vacancy_desc import VacancyDesc


@dataclass
class Vacancy(VacancyDesc):
    _experience: str
    _salary: str
    _key_skills: str

    @property
    def experience(self) -> str:
        return self._experience

    @experience.setter
    def experience(self, value: str):
        self._experience = value

    @property
    def salary(self) -> str:
        return self._salary

    @salary.setter
    def salary(self, value: str):
        self._salary = value

    @property
    def key_skills(self) -> str:
        return self._key_skills

    @key_skills.setter
    def key_skills(self, value: str):
        self._key_skills = value


