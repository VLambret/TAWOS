from cumulative_flow import CumulativeFlow


class NoEstimateForecast:
    def __init__(self, cumulative_flow: CumulativeFlow, using_last_days: int, on_the_next_days: int):
        self.cumulative_flow = cumulative_flow
        self.number_of_day_used_for_velocity = using_last_days
        self.number_of_days_in_the_future = on_the_next_days

    def forecast_on_day(self, forecast_day) -> float:
        total_closed_tasks_that_day = self.cumulative_flow.get_total_closed_task_on_day(forecast_day)

        first_day_of_velocity_interval = forecast_day - self.number_of_day_used_for_velocity
        closed_before_interval = self.cumulative_flow.get_total_closed_task_on_day(first_day_of_velocity_interval)

        closed_during_interval = total_closed_tasks_that_day - closed_before_interval
        task_velocity_per_day = closed_during_interval / self.number_of_day_used_for_velocity

        return total_closed_tasks_that_day + task_velocity_per_day * self.number_of_days_in_the_future
