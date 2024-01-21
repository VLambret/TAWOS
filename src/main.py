#! /usr/bin/python3

import sys
from datetime import date, datetime
from pathlib import Path
from statistics import mean

from graph import save_as_graph
from time_series.normalized_time_series import NormalizedTimeSeries
from time_series.indexed_dated_values import DatedValuesType, CumulativeTimeSeries
from forecasts.no_estimate_forecast import NoEstimateForecast
from time_series.time_series import TimeSeries


def old_to_new(all_data_to_plot: dict[str, DatedValuesType]) -> dict[str, CumulativeTimeSeries]:
    all_data_to_plot = {
        k: CumulativeTimeSeries(v)
        for k, v in all_data_to_plot.items()
    }
    return all_data_to_plot


class Project:
    def __init__(self, dates_in_csv_file: str):
        dates_in_csv_file = Path(dates_in_csv_file)
        dates = load_dates_from(dates_in_csv_file)

        self.folder: Path = dates_in_csv_file.parent
        self.name = dates_in_csv_file.name.replace('_', " ").removesuffix(".csv")
        self.activity = NormalizedTimeSeries(dates)


def load_dates_from(project_csv: Path) -> list[date]:
    with project_csv.open('r') as f:
        return [datetime.strptime(d.strip(), "%Y-%m-%d").date() for d in f.readlines()]


def main():
    project = Project(sys.argv[1])

    ################################################################################
    # REALITY
    ################################################################################

    real_cumulated_closed_tasks: TimeSeries

    ################################################################################
    # USING TOTAL CUMULATED COMPLETED TASKS
    ################################################################################

    actual_total_completed_tasks_per_day = project.activity.cumulated_completed_tasks
    all_total_completed_tasks_per_day_estimates = get_all_total_completed_tasks_per_day_estimates(project.activity)

    all_estimates_to_plot: dict[str, CumulativeTimeSeries] = {"Actual": actual_total_completed_tasks_per_day}
    for n in [180, 360]:
        all_estimates_to_plot[f'{n} days'] = all_total_completed_tasks_per_day_estimates[n]

    save_as_graph(project, "cumulated completed task forecasts", all_estimates_to_plot)

    # Signed MMRE
    signed_mmre_to_plot = compute_signed_mmre(actual_total_completed_tasks_per_day,
                                       all_estimates_to_plot)
    save_as_graph(project,
                  "cumulated completed task forecasts signed MMRE",
                  signed_mmre_to_plot)

    # MMRE
    mmre_to_plot = compute_mmre(actual_total_completed_tasks_per_day,
                                all_estimates_to_plot)
    save_as_graph(project,
                  "cumulated completed task forecasts MMRE",
                  mmre_to_plot)

    # MMRE Quality
    mmre_quality = {"MMRE quality": CumulativeTimeSeries(
        {
            period: mean(values.compute_mmre_compared_to_reference(actual_total_completed_tasks_per_day).get_values())
            for period, values in all_total_completed_tasks_per_day_estimates.items()
        })
    }
    save_as_graph(project,
                  "Average MMRE for each period",
                  mmre_quality)

    ################################################################################
    # USING COMPLETED TASK IN THE LAST PERIOD
    ################################################################################

    all_completed_tasks_in_last_period_estimates = compute_completed_task_last_period(all_estimates_to_plot)
    save_as_graph(project,
                  f"Tasks completed in the last period for each day",
                  all_completed_tasks_in_last_period_estimates)

    # periodical MMRE

    all_periodical_mmre: dict[str, CumulativeTimeSeries] = {}
    for period, estimates in all_total_completed_tasks_per_day_estimates.items():
        periodical_reference = actual_total_completed_tasks_per_day.compute_completed_task_last_period(period)
        periodical_tasks = estimates.compute_completed_task_last_period(period)
        periodical_mmre = periodical_tasks.compute_mmre_compared_to_reference(periodical_reference)
        all_periodical_mmre[f'{period} days'] = periodical_mmre

    save_as_graph(project,
                  "All periodical_mmre",
                  all_periodical_mmre)

    # periodical MMRE quality

    all_periodical_mmre_quality = {"MMRE quality": CumulativeTimeSeries(
        {
            period: mean(values.compute_mmre_compared_to_reference(actual_total_completed_tasks_per_day).get_values())
            for period, values in all_periodical_mmre.items()
        })
    }
    save_as_graph(project,
                  "Periodical MMRE quality",
                  all_periodical_mmre_quality)



def compute_completed_task_last_period(all_estimates_to_plot):

    def period(key: str):
        if "days" in key:
            return int(key.removesuffix("days"))
        else:
            return 360

    estimates_with_periodic_total = {
        k: v.compute_completed_task_last_period(period(k))
        for k, v in all_estimates_to_plot.items()
    }
    return estimates_with_periodic_total


def compute_mmre(reference, estimates):
    return {
        tag: estimate.compute_mmre_compared_to_reference(reference) for tag, estimate
        in
        estimates.items()
    }


def compute_signed_mmre(reference, estimates):
    return {
        tag: estimate.compute_signed_mmre_compared_to_reference(reference) for tag, estimate
        in
        estimates.items()
    }


def get_all_total_completed_tasks_per_day_estimates(project_activity):
    estimate_periods = [1, 5, 10, 20, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 720]
    all_estimates: dict[int: CumulativeTimeSeries] = {
        period: NoEstimateForecast(project_activity, period, period).forecast_for_all_days()
        for period in estimate_periods
    }
    return all_estimates


if __name__ == "__main__":
    main()
