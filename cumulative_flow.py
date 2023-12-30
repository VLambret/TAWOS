from collections import Counter
from datetime import date, timedelta

from pandas import date_range


class CumulativeFlow:
    def __init__(self, dates: list[date]):
        self.first_day: date = min(dates)
        self.last_day: date = max(dates)

        closed_tasks_per_day = dict(Counter(dates))

        project_range = [d.date() for d in date_range(self.first_day, self.last_day)]

        result: dict[date: int] = {d: 0 for d in project_range}

        total_completed_task: int = 0
        for d in project_range:
            total_completed_task += closed_tasks_per_day.get(d, 0)
            result[d] = total_completed_task

        self.total_closed_task_per_day: dict[date, int] = result

    def get_total_closed_task_on_day(self, day_number: int) -> int:
        date_from_day_number = self.first_day + timedelta(days=day_number - 1)

        if date_from_day_number < self.first_day:
            return 0

        if date_from_day_number > self.last_day:
            return self.total_closed_task_per_day[self.last_day]

        if date_from_day_number not in self.total_closed_task_per_day:
            raise IndexError("date number outside of project")

        return self.total_closed_task_per_day[date_from_day_number]

    def get_closed_tasks_in(self, start, end) -> int:
        return self.get_total_closed_task_on_day(end) - self.get_total_closed_task_on_day(start)

