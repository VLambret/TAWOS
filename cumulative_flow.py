from collections import Counter
from datetime import date

from pandas import date_range


def get_cumulative_flow(dates: list[date]) -> dict[date, int]:
    first_completed_task = min(dates)
    last_completed_task = max(dates)

    closed_tasks_per_day = dict(Counter(dates))

    project_range = [d.date() for d in date_range(first_completed_task, last_completed_task)]

    result: dict[date: int] = {d: 0 for d in project_range}

    total_completed_task: int = 0
    for d in project_range:
        total_completed_task += closed_tasks_per_day.get(d, 0)
        result[d] = total_completed_task

    return result
