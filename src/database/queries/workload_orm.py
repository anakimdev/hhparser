from src.database.core.engine import async_session
from src.database.models.dictionaries import WorkloadTable


class WorkloadOrm():

    @staticmethod
    async def insert_workload():
        async with async_session() as session:
            workload_1 = WorkloadTable(key="full", title="Полная занятость")
            workload_2 = WorkloadTable(key="part", title="Частичная занятость")
            workload_3 = WorkloadTable(key="project", title="Проектная работа")
            workload_4 = WorkloadTable(key="volunteer", title="Волонтерство")
            workload_5 = WorkloadTable(key="probation", title="Стажировка")

            session.add_all([workload_1, workload_2, workload_3, workload_4, workload_5])
            await session.commit()
