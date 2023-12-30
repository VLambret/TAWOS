from datetime import date

from pandas import date_range

from cumulative_flow import CumulativeFlow
from no_estimate_forecast import NoEstimateForecast


def project_closing_one_task_each_day():
    each_date_once_in_interval = [d.date() for d in date_range(
        date(2023, 1, 1),
        date(2023, 1, 31),
    )]

    return CumulativeFlow(each_date_once_in_interval)


class TestNoEstimateForecast:
    def test_future_can_be_forecasted_from_the_past(self):
        project = project_closing_one_task_each_day()
        forecaster = NoEstimateForecast(project, 1, 1)

        assert 11 == forecaster.forecast_on_day(10)

    def test_future_can_be_projected_from_the_past_other_case(self):
        project = project_closing_one_task_each_day()
        forecaster = NoEstimateForecast(project, 5, 10)

        assert 20 == forecaster.forecast_on_day(10)
