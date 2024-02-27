from dataclasses import dataclass

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


def optimization_result(request_data: dict) -> list[str]:
    results = None

    for item in request_data.get('items'):
        if results is None:
            results = []

        name = f"Название компании: {item['employer']['name']}"
        experience = f"Требуемый опыт работы: {item['experience']['name']}"

        if item.get('salary').get('to') is None:
            salary = f"Заработная плата: от {item['salary']['from']}"
        else:
            salary = f"Заработная плата: от {item['salary']['from']} до {item['salary']['to']}"

        des_string = ';\n - '.join(v.lstrip(' - ') for v in str(item['snippet']['responsibility']).split('.')).rstrip(
            '\n - ')
        description = f"Особенности работы: \n - {des_string}"

        key_string = ';\n - '.join(v.lstrip(' - ') for v in str(item['snippet']['requirement']).split('.')).rstrip(
            '\n - ')
        key_skills = f"Ключевые навыки: \n - {key_string}"

        link = f"Ссылка: {item.get('alternate_url')}"

        results.append(Vacancy(name, experience, salary, description, key_skills, link).__str__())

    return results
