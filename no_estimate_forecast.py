from cumulative_flow import CumulativeFlow


class NoEstimateForecast:
    def __init__(self,
                 cumulative_flow: CumulativeFlow,
                 using_last_days: int,
                 on_the_next_days: int,
                 use_blind_spot_workaround=False):
        self.cumulative_flow = cumulative_flow
        self.number_of_day_used_for_velocity = using_last_days
        self.number_of_days_in_the_future = on_the_next_days
        self.use_blind_spot_workaround = use_blind_spot_workaround

    def _forecast_on_day(self, forecast_day: int, number_of_days_in_the_future) -> float:
        if forecast_day <= 0:
            return 0.0

        total_closed_tasks_that_day = self.cumulative_flow.get_total_closed_task_on_day(forecast_day)
        velocity = self._get_velocity_on_day(forecast_day)
        return total_closed_tasks_that_day + velocity * number_of_days_in_the_future

    def forecast_on_day(self, forecast_day) -> float:
        return self._forecast_on_day(forecast_day, self.number_of_days_in_the_future)

    def forecast_for_day(self, day_to_forecast_for) -> float:
        day_to_forecast_on = day_to_forecast_for - self.number_of_days_in_the_future
        number_of_days_in_the_future = self.number_of_days_in_the_future

        if self.use_blind_spot_workaround:
            day_to_forecast_on = max(day_to_forecast_on, 1)
            if day_to_forecast_on == 1:
                number_of_days_in_the_future = 0
            if day_to_forecast_on == 2:
                number_of_days_in_the_future = 1


        return self._forecast_on_day(day_to_forecast_on, number_of_days_in_the_future)

    def forecast_for_all_days(self) -> list[float]:
        all_days_to_forecast_to = range(1, len(self.cumulative_flow.total_closed_task_per_day) + 1)
        return [self.forecast_for_day(d) for d in (all_days_to_forecast_to)]

    def _get_velocity_on_day(self, forecast_day) -> float:
        first_day_of_velocity_interval = max(0, forecast_day - self.number_of_day_used_for_velocity)

        tasks_closed_in_interval = self.cumulative_flow.get_closed_tasks_in(first_day_of_velocity_interval, forecast_day)
        days_in_interval = (forecast_day - first_day_of_velocity_interval)

        return tasks_closed_in_interval / days_in_interval
