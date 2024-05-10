from dataclasses import dataclass


@dataclass
class VacancyDesc:
    _company_name: str
    _description: str
    _link: str

    def __str__(self):
        return self.description

    @property
    def link(self) -> str:
        return self._link

    @link.setter
    def link(self, value: str):
        self._link = value

    @property
    def company_name(self) -> str:
        return self._company_name

    @company_name.setter
    def company_name(self, value: str):
        self._company_name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value



