from src.database.core.engine import async_session
from src.database.models.common_dicts import WorkloadsTable


class WorkloadOrm:

    @staticmethod
    async def insert_workload():
        async with async_session() as session:
            workload_1 = WorkloadsTable(key="full", title="Полная занятость")
            workload_2 = WorkloadsTable(key="part", title="Частичная занятость")
            workload_3 = WorkloadsTable(key="project", title="Проектная работа")
            workload_4 = WorkloadsTable(key="volunteer", title="Волонтерство")
            workload_5 = WorkloadsTable(key="probation", title="Стажировка")

            session.add_all([workload_1, workload_2, workload_3, workload_4, workload_5])
            await session.commit()
