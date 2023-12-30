from cumulative_flow import CumulativeFlow


class NoEstimateForecast:
    def __init__(self, cumulative_flow: CumulativeFlow, using_last_days: int, on_the_next_days: int):
        self.cumulative_flow = cumulative_flow
        self.number_of_day_used_for_velocity = using_last_days
        self.number_of_days_in_the_future = on_the_next_days

    def forecast_on_day(self, forecast_day) -> float:
        if forecast_day <= 0:
            return 0.0

        total_closed_tasks_that_day = self.cumulative_flow.get_total_closed_task_on_day(forecast_day)

        velocity = self._get_velocity_on_day(forecast_day)

        return total_closed_tasks_that_day + velocity * self.number_of_days_in_the_future

    def _get_velocity_on_day(self, forecast_day) -> float:
        first_day_of_velocity_interval = max(0, forecast_day - self.number_of_day_used_for_velocity)

        tasks_closed_in_interval = self.cumulative_flow.get_closed_tasks_in(first_day_of_velocity_interval, forecast_day)
        days_in_interval = (forecast_day - first_day_of_velocity_interval)

        return tasks_closed_in_interval / days_in_interval
