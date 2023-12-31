from datetime import date, timedelta

from pandas import date_range

from cumulative_flow import CumulativeFlow
from no_estimate_forecast import NoEstimateForecast


def project_closing_one_task_each_day(project_duration):
    start = date(2023, 1, 1)
    each_date_once_in_interval = [d.date() for d in date_range(
        start,
        start + timedelta(days=project_duration - 1),
    )]

    return CumulativeFlow(each_date_once_in_interval)


class TestNoEstimateForecastAllDays:
    def test_future_can_be_forecasted_from_the_past(self):
        project = project_closing_one_task_each_day(5)
        forecaster = NoEstimateForecast(project, 1, 1)

        assert forecaster.forecast_for_day(1) == 0.0
        assert forecaster.forecast_for_day(2) == 2.0
        assert forecaster.forecast_for_day(3) == 3.0
        assert forecaster.forecast_for_day(4) == 4.0
        assert forecaster.forecast_for_day(5) == 5.0

        expected_forecast = [0.0, 2.0, 3.0, 4.0, 5.0]
        actual_forecast = forecaster.forecast_for_all_days()
        assert actual_forecast == expected_forecast

    def test_get_all_days_to_forecast_on_without_initial_hack(self):
        project = project_closing_one_task_each_day(5)
        forecaster = NoEstimateForecast(project, 3, 3)

        assert forecaster._get_all_days_to_forecast_on() == [-2, -1, 0, 1, 2]


class TestNoEstimateForecastSingleDay:
    def test_future_can_be_forecasted_from_the_past(self):
        project = project_closing_one_task_each_day(5)
        forecaster = NoEstimateForecast(project, 1, 1)

        assert forecaster.forecast_on_day(1) == 2.0
        assert forecaster.forecast_on_day(2) == 3.0
        assert forecaster.forecast_on_day(3) == 4.0
        assert forecaster.forecast_on_day(4) == 5.0
        assert forecaster.forecast_on_day(5) == 6.0

    def test_future_can_be_projected_from_the_past_other_case(self):
        project = project_closing_one_task_each_day(31)
        forecaster = NoEstimateForecast(project, 5, 10)

        assert forecaster.forecast_on_day(10) == 20.0

    def test_only_pasts_days_inside_project_are_used_for_velocity(self):
        project = project_closing_one_task_each_day(31)
        forecaster = NoEstimateForecast(project, 10, 10)

        assert forecaster.forecast_on_day(0) == 0.0
        assert forecaster.forecast_on_day(1) == 11.0
        assert forecaster.forecast_on_day(5) == 15.0

    def test_it_s_possible_to_forecast_after_the_project_end(self):
        project = project_closing_one_task_each_day(31)
        forecaster = NoEstimateForecast(project, 10, 10)

        assert forecaster.forecast_on_day(40) == 32.0
        assert forecaster.forecast_on_day(50) == 31.0
