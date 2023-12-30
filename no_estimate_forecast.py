from datetime import date

from cumulative_flow import CumulativeFlow


class ForecastUsingLast:

    def __init__(self, task_velocity_per_day: float):
        self.task_velocity_per_day = task_velocity_per_day

    def on_next_days(self, number_of_days) -> int:
        return self.task_velocity_per_day * number_of_days


class ForecastOnDay:

    def __init__(self, flow, day_number: date):
        self.cumulative_flow: CumulativeFlow = flow
        self.day_number: date = day_number

    def using_last_days(self, number_of_past_days) -> ForecastUsingLast:
        first_day = self.cumulative_flow.keys()[0]
        closed_that_day = self.cumulative_flow[first_day + self.day_number]
        closed_before_interval = self.cumulative_flow[first_day + (self.day_number - number_of_past_days)]
        closed_during_interval = closed_that_day - closed_before_interval

        task_velocity_per_day = closed_during_interval / number_of_past_days
        return ForecastUsingLast(task_velocity_per_day)


class NoEstimateForecast:
    def __init__(self, cumulative_flow: CumulativeFlow):
        self.cumulative_flow = cumulative_flow

    def forecast_on_day(self, forecast_day) -> ForecastOnDay:
        return ForecastOnDay(self.cumulative_flow, forecast_day)
