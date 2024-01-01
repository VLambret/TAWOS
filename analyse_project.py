#! /usr/bin/python3
import sys
from datetime import date, datetime
from pathlib import Path
from statistics import mean

import matplotlib
import matplotlib.figure

from cumulative_flow import CumulativeFlow
from indexed_dated_values import DatedValuesType, IndexedDatedValues
from no_estimate_forecast import NoEstimateForecast


def old_to_new(all_data_to_plot: dict[str, DatedValuesType]) -> dict[str, IndexedDatedValues]:
    all_data_to_plot = {
        k: IndexedDatedValues(v)
        for k, v in all_data_to_plot.items()
    }
    return all_data_to_plot


class Project:
    def __init__(self, dates_in_csv_file: str):
        dates_in_csv_file = Path(dates_in_csv_file)
        dates = load_dates_from(dates_in_csv_file)

        self.folder: Path = dates_in_csv_file.parent
        self.name = dates_in_csv_file.name.replace('_', " ").removesuffix(".csv")
        self.activity = CumulativeFlow(dates)


def save_as_graph(project, title: str, all_data_to_plot: dict[str, IndexedDatedValues]):
    figure = matplotlib.figure.Figure(figsize=(8, 6))

    filename = project.folder / (title.replace(' ', '_') + ".png")

    figure_axis = figure.add_subplot()
    figure.suptitle(f"{project.name} - {title}")
    figure_axis.set_xlabel('Date')
    figure_axis.set_ylabel('# of Completed issues')

    for label, data in all_data_to_plot.items():
        estimates_dates = data.get_dates()
        estimates_values = data.get_values()
        figure_axis.plot(estimates_dates, estimates_values, label=label)

    figure_axis.legend()

    figure.savefig(filename, dpi=300)


def load_dates_from(project_csv: Path) -> list[date]:
    with project_csv.open('r') as f:
        return [datetime.strptime(d.strip(), "%Y-%m-%d").date() for d in f.readlines()]


def main():
    project = Project(sys.argv[1])

    ###################
    # Estimates part
    ###################

    actual_total_completed_tasks_per_day = project.activity.cumulated_completed_tasks
    all_total_completed_tasks_per_day_estimates = get_all_total_completed_tasks_per_day_estimates(project.activity)

    all_estimates_to_plot: dict[str, IndexedDatedValues] = {"Actual": actual_total_completed_tasks_per_day}
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
    mmre_quality = {"MMRE quality": IndexedDatedValues(
        {
            period: mean(values.compute_mmre_compared_to_reference(actual_total_completed_tasks_per_day).get_values())
            for period, values in all_total_completed_tasks_per_day_estimates.items()
        })
    }
    save_as_graph(project,
                  "Average MMRE for each period",
                  mmre_quality)


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
    all_estimates: dict[int: IndexedDatedValues] = {
        period: NoEstimateForecast(project_activity, period, period).forecast_for_all_days()
        for period in estimate_periods
    }
    return all_estimates


main()
