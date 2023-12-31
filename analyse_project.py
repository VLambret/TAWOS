#! /usr/bin/python3
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

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


@dataclass
class GraphLabels:
    title: str


def show_graph(graph_name: GraphLabels, filename: Path, all_data_to_plot: dict[str, IndexedDatedValues]):
    figure = matplotlib.figure.Figure(figsize=(8, 6))

    figure_axis = figure.add_subplot()
    figure.suptitle(graph_name.title)
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

    project_folder = project_csv.parent
    project_name = project_csv.name.replace('_', " ").removesuffix(".csv")

    dates = load_dates_from(project_csv)
    project_activity = CumulativeFlow(dates)

    ###################
    # Estimates part
    ###################

    actual = project_activity.cumulated_completed_tasks

    estimate_periods = [1, 5, 10, 20, 30, 60, 90, 180, 240, 360]
    all_estimates = {
        period: NoEstimateForecast(project_activity, period, period).forecast_for_all_days()
        for period in estimate_periods
    }

    all_estimates_to_plot: dict[str, IndexedDatedValues] = {"Actual": actual}

    for n in [30, 180, 360]:
        forecaster = NoEstimateForecast(project_activity, n, n)
        estimates = forecaster.forecast_for_all_days()
        tag = f'{n} days'
        all_estimates_to_plot[tag] = estimates

    project_graph_file = project_folder / "graph_actual_work_and_estimates"
    labels = GraphLabels(title=f"{project_name} - cumulated completed task forecasts")
    show_graph(labels, project_graph_file, all_estimates_to_plot)

    ###################
    # Signed MMRE part
    ###################

    mmre_to_plot: dict[str, IndexedDatedValues] = {
        tag: estimate.compute_signed_mmre_compared_to_reference(actual) for tag, estimate in
        all_estimates_to_plot.items()
    }

    mmre_graph_file = project_folder / "graph_signed_mmre"
    labels = GraphLabels(title=f"{project_name} - cumulated completed task forecasts signed MMRE")
    show_graph(labels, mmre_graph_file, mmre_to_plot)

    ###################
    # MMRE part
    ###################

    mmre_to_plot: dict[str, IndexedDatedValues] = {
        tag: estimate.compute_mmre_compared_to_reference(actual) for tag, estimate in
        all_estimates_to_plot.items()
    }

    mmre_graph_file = project_folder / "graph_mmre"
    labels = GraphLabels(title=f"{project_name} - cumulated completed task forecasts MMRE")
    show_graph(labels, mmre_graph_file, mmre_to_plot)


main()
