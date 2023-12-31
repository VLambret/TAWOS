#! /usr/bin/python3
import sys
from datetime import date, datetime
from pathlib import Path

import matplotlib
import matplotlib.figure

from cumulative_flow import CumulativeFlow
from indexed_dated_values import DatedValuesType, IndexedDatedValues
from mmre import compute_all_signed_mmre_legacy
from no_estimate_forecast import NoEstimateForecast


def old_to_new(all_data_to_plot: dict[str, DatedValuesType]) -> dict[str, IndexedDatedValues]:
    all_data_to_plot = {
        k: IndexedDatedValues(v)
        for k, v in all_data_to_plot.items()
    }
    return all_data_to_plot


def show_graph(filename: Path, all_data_to_plot: dict[str, IndexedDatedValues]):
    figure = matplotlib.figure.Figure(figsize=(8, 6))

    figure_axis = figure.add_subplot()
    figure.suptitle(f'{filename} - Completed issues over time')
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
    project_csv = Path(sys.argv[1])

    dates = load_dates_from(project_csv)
    project_activity = CumulativeFlow(dates)

    cumulated_completed_task_per_day: DatedValuesType = project_activity.total_closed_task_per_day

    ###################
    # Estimates part
    ###################

    actual = project_activity.cumulated_completed_tasks
    all_estimates_to_plot: dict[str, IndexedDatedValues] = {"Actual": actual}

    for n in [30, 180, 360]:
        forecaster = NoEstimateForecast(project_activity, n, n)
        estimates = forecaster.forecast_for_all_days()
        tag = f'{n} days forecast'
        all_estimates_to_plot[tag] = estimates

    project_graph_file = Path(sys.argv[1]).parent / "graph_actual_work_and_estimates"
    show_graph(project_graph_file, all_estimates_to_plot)

    ###################
    # MRE part
    ###################

    mmre_to_plot: dict[str, IndexedDatedValues] = {
        tag: estimate.compute_signed_mmre_compared_to_reference(actual) for tag, estimate in all_estimates_to_plot.items()
    }

    ideal_mmre_legacy = {k: 0.0 for k, v in cumulated_completed_task_per_day.items()}
    mmre_to_plot_legacy = {"Actual": ideal_mmre_legacy}

    for n in [30, 180, 360]:
        forecaster = NoEstimateForecast(project_activity, n, n)
        estimates_legacy = forecaster.forecast_for_all_days_legacy()

        mmre_legacy = compute_all_signed_mmre_legacy(list(cumulated_completed_task_per_day.values()), estimates_legacy)

        mmre_with_dates = {}
        for index, day in enumerate(cumulated_completed_task_per_day.keys()):
            mmre_with_dates[day] = mmre_legacy[index]

        tag = f'{n} days forecast'

        mmre_to_plot_legacy[tag] = mmre_with_dates

    mmre_graph_file = Path(sys.argv[1]).parent / "graph_mmre"
    show_graph(mmre_graph_file, old_to_new(mmre_to_plot_legacy))


main()
