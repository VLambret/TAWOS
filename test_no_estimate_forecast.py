from datetime import date

from pandas import date_range

from cumulative_flow import CumulativeFlow
from no_estimate_forecast import NoEstimateForecast


def project_closing_one_task_each_day():
    each_date_once_in_interval = list(date_range(
        date(2023, 1, 1),
        date(2023, 1, 31),
    ))

    return CumulativeFlow(each_date_once_in_interval)


class TestNoEstimateForecast:
    def test_future_can_be_projected_from_the_past(self):
        project = project_closing_one_task_each_day()
        forecaster = NoEstimateForecast(project)

        #five_day_forecast = (forecaster.forecast_on_day(10)
        #                     .using_last_days(1)
        #                     .on_next_days(1))

        #assert 11 == five_day_forecast
