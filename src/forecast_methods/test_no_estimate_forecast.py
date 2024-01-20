from datetime import date, timedelta

import pytest
from pandas import date_range

from model.normalized_time_series import NormalizedTimeSeries
from forecast_methods.no_estimate_forecast import NoEstimateForecast


def project_completing_exactly_one_task_each_day(project_duration):
    start = date(2023, 1, 1)
    each_date_once_in_interval = [d.date() for d in date_range(
        start,
        start + timedelta(days=project_duration - 1),
    )]

    return NormalizedTimeSeries(each_date_once_in_interval)


def project_increasing_velocity_each_day(project_duration):
    start = date(2023, 1, 1)

    one_more_task_completed_each_day = []
    for index, d in enumerate(date_range(start, start + timedelta(days=project_duration - 1))):
        one_more_task_completed_each_day += [d.date()] * index

    return NormalizedTimeSeries(one_more_task_completed_each_day)


class TestPerfectProject_WithInitialWorkaround:
    project = project_completing_exactly_one_task_each_day(10)
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
        assert self.perfect_project_forecaster.forecast_for_all_days_legacy() == expected


class TestPerfectProject_NoInitialWorkaround:
    project = project_completing_exactly_one_task_each_day(10)
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
        assert self.perfect_project_forecaster.forecast_for_all_days_legacy() == expected


class TestSpeedingUpProject_WithInitialWorkaround:
    project = project_increasing_velocity_each_day(25)
    project_speeding_up = NoEstimateForecast(project, 10, 10, use_blind_spot_workaround=True)

    @pytest.mark.parametrize("day, expected", [
        (1, 1.0),
        (2, 2.0),
        (3, 3.0),
        (4, 4.0),
        (5, 5.0),
        (6, 9.0),
        (7, 10.5),
        (8, 12.0),
        (9, 13.5),
        (10, 15.0),
    ])
    def test_internal_forecast_on_day(self, day, expected):
        assert self.project_speeding_up.forecast_for_day(day) == expected

    # NOTE: non-regression test
    def test_forecast_for_all_days(self):
        expected = [1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    9.0,
                    10.5,
                    12.0,
                    13.5,
                    15.0,
                    22.0,
                    24.0,
                    26.0,
                    35.0,
                    45.0,
                    56.0,
                    68.0,
                    81.0,
                    95.0,
                    110.0,
                    131.0,
                    153.0,
                    176.0,
                    200.0]
        assert self.project_speeding_up.forecast_for_all_days_legacy() == expected
