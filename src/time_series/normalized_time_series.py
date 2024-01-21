from collections import Counter
from datetime import date, timedelta

from pandas import date_range

from time_series.cumulative_time_series import DatedValuesType, CumulativeTimeSeries


class NormalizedTimeSeries:
    def __init__(self, completed_task_dates: list[date], filter=False):

        # Filter out last last project trail
        if filter:
            completed_task_dates = sorted(completed_task_dates)
            percentage_to_remove = 1
            number_of_last_tasks_to_remove: int = int((len(completed_task_dates) * percentage_to_remove) / 100)
            completed_task_dates = completed_task_dates[number_of_last_tasks_to_remove:-number_of_last_tasks_to_remove]

        self.first_day: date = min(completed_task_dates)
        self.last_day: date = max(completed_task_dates)

        closed_tasks_per_day = dict(Counter(completed_task_dates))

        # Filter out large number of closed tasks on a single day. Most likely an automated removal
        if filter:
            for key, value in closed_tasks_per_day.items():
                if value > 100:
                    closed_tasks_per_day[key] = 0

        project_range = [d.date() for d in date_range(self.first_day, self.last_day)]

        result: DatedValuesType = {d: 0 for d in project_range}

        total_completed_task: int = 0
        for d in project_range:
            total_completed_task += closed_tasks_per_day.get(d, 0)
            result[d] = total_completed_task

        self.total_closed_task_per_day: DatedValuesType = result
        self.cumulated_completed_tasks: CumulativeTimeSeries = CumulativeTimeSeries(result)

    def get_total_completed_task_on_day(self, day_number: int) -> int | float:
        date_from_day_number = self.first_day + timedelta(days=day_number - 1)

        if date_from_day_number < self.first_day:
            return 0

        if date_from_day_number > self.last_day:
            return self.total_closed_task_per_day[self.last_day]

        return self.total_closed_task_per_day[date_from_day_number]

    def get_closed_tasks_in(self, start, end) -> int | float:
        return self.get_total_completed_task_on_day(end) - self.get_total_completed_task_on_day(start)
