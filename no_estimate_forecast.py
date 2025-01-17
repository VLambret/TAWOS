import math
from datetime import date

from cumulative_flow import CumulativeFlow
from indexed_dated_values import IndexedDatedValues


class NoEstimateForecast:
    def __init__(self,
                 cumulative_flow: CumulativeFlow,
                 using_last_days: int,
                 on_the_next_days: int,
                 use_blind_spot_workaround=True):
        self.cumulative_flow = cumulative_flow
        self.number_of_day_used_for_velocity = using_last_days
        self.number_of_days_in_the_future = on_the_next_days
        self.use_blind_spot_workaround = use_blind_spot_workaround
        self.blind_spot_percent_to_use = 0.20

    def _forecast_on_day(self, forecast_day: int, number_of_days_in_the_future) -> float:
        if forecast_day <= 0:
            return 0.0

        total_closed_tasks_that_day = self.cumulative_flow.get_total_completed_task_on_day(forecast_day)
        velocity = self._get_velocity_on_day(forecast_day)
        return total_closed_tasks_that_day + velocity * number_of_days_in_the_future

    def forecast_for_day(self, day_to_forecast_for) -> float:
        day_to_forecast_on = day_to_forecast_for - self.number_of_days_in_the_future
        number_of_days_in_the_future = self.number_of_days_in_the_future

        if self.use_blind_spot_workaround:
            if day_to_forecast_on <= self.number_of_days_in_the_future * self.blind_spot_percent_to_use:
                day_to_forecast_on = max(day_to_forecast_on, math.ceil(day_to_forecast_for * self.blind_spot_percent_to_use))

            overflow = day_to_forecast_on + self.number_of_days_in_the_future - day_to_forecast_for
            if overflow >= 0:
                number_of_days_in_the_future = self.number_of_days_in_the_future - overflow

        return self._forecast_on_day(day_to_forecast_on, number_of_days_in_the_future)

    def forecast_for_all_days_legacy(self) -> list[float]:
        return [float(v) for v in (self.forecast_for_all_days().get_values())]

    def forecast_for_all_days(self) -> IndexedDatedValues:
        dates: list[date] = self.cumulative_flow.cumulated_completed_tasks.get_dates()
        result = {date_value: self.forecast_for_day(day + 1) for day, date_value in enumerate(dates)}
        return IndexedDatedValues(result)

    def _get_velocity_on_day(self, forecast_day) -> float:
        first_day_of_velocity_interval = max(0, forecast_day - self.number_of_day_used_for_velocity)

        tasks_closed_in_interval = self.cumulative_flow.get_closed_tasks_in(first_day_of_velocity_interval, forecast_day)
        days_in_interval = (forecast_day - first_day_of_velocity_interval)

        return tasks_closed_in_interval / days_in_interval
