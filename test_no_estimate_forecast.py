from datetime import date, timedelta

import pytest
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


class TestWithInitialWorkaround:
    project = project_closing_one_task_each_day(10)
    perfect_project_forecaster = NoEstimateForecast(project, 3, 3, use_blind_spot_workaround=True)

    @pytest.mark.parametrize("on_day, days_in_the_future, expected", [
        (1, 0, 1.0),
        (1, 1, 2.0),
        (1, 2, 3.0),
        (1, 3, 4.0),
        (2, 3, 5.0),
    ])
    def test_internal_forecast_on_day(self, on_day, days_in_the_future, expected):
        assert self.perfect_project_forecaster._forecast_on_day(on_day, days_in_the_future) == expected

    @pytest.mark.parametrize("day, expected", [
        (1, 4.0),
        (2, 5.0),
        (3, 6.0),
        (4, 7.0),
        (5, 8.0),
    ])
    def test_forecast_on_day(self, day, expected):
        assert self.perfect_project_forecaster.forecast_on_day(day) == expected

    @pytest.mark.parametrize("day, expected", [
        (1, 1.0),
        (2, 2.0),
        (3, 3.0),
        (4, 4.0),
        (5, 5.0),
    ])
    def test_forecast_for_day(self, day, expected):
        assert self.perfect_project_forecaster.forecast_for_day(day) == expected

    def test_forecast_for_all_days(self):
        expected = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        assert self.perfect_project_forecaster.forecast_for_all_days() == expected


class TestWithNoInitialWorkaround:
    project = project_closing_one_task_each_day(10)
    perfect_project_forecaster = NoEstimateForecast(project, 3, 3, use_blind_spot_workaround=False)

    @pytest.mark.parametrize("on_day, days_in_the_future, expected", [
        (1, 0, 1.0),
        (1, 1, 2.0),
        (1, 2, 3.0),
        (1, 3, 4.0),
        (2, 3, 5.0),
    ])
    def test_internal_forecast_on_day(self, on_day, days_in_the_future, expected):
        assert self.perfect_project_forecaster._forecast_on_day(on_day, days_in_the_future) == expected

    @pytest.mark.parametrize("day, expected", [
        (1, 4.0),
        (2, 5.0),
        (3, 6.0),
        (4, 7.0),
        (5, 8.0),
    ])
    def test_forecast_on_day(self, day, expected):
        assert self.perfect_project_forecaster.forecast_on_day(day) == expected

    @pytest.mark.parametrize("day, expected", [
        (1, 0.0),
        (2, 0.0),
        (3, 0.0),
        (4, 4.0),
        (5, 5.0),
    ])
    def test_forecast_for_day(self, day, expected):
        assert self.perfect_project_forecaster.forecast_for_day(day) == expected

    def test_forecast_for_all_days(self):
        expected = [0.0, 0.0, 0.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        assert self.perfect_project_forecaster.forecast_for_all_days() == expected


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
