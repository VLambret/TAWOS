#! /usr/bin/python3
import sys
from datetime import date, datetime
from pathlib import Path

import matplotlib
import matplotlib.figure

from cumulative_flow import CumulativeFlow, DatedValues
from mmre import compute_all_signed_mmre
from no_estimate_forecast import NoEstimateForecast


def show_graph(filename: Path, all_data_to_plot: dict[str, DatedValues]):
    figure = matplotlib.figure.Figure(figsize=(8, 6))

    figure_axis = figure.add_subplot()
    figure.suptitle(f'{filename} - Completed issues over time')
    figure_axis.set_xlabel('Date')
    figure_axis.set_ylabel('# of Completed issues')

    for label, data in all_data_to_plot.items():
        estimates_dates = list(data.keys())
        estimates_values = list(data.values())
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

    cumulated_completed_task_per_day = project_activity.total_closed_task_per_day

    all_sets_to_plot = {"Actual": cumulated_completed_task_per_day}
    ideal_mmre = {k: 0.0 for k, v in cumulated_completed_task_per_day.items()}
    mmre_to_plot = {"Actual": ideal_mmre}

    for n in [30, 180, 360]:
        forecaster = NoEstimateForecast(project_activity, n, n)
        estimates = forecaster.forecast_for_all_days()

        estimates_with_dates = {}
        for index, day in enumerate(cumulated_completed_task_per_day.keys()):
            estimates_with_dates[day] = estimates[index]

        mmre = compute_all_signed_mmre(list(cumulated_completed_task_per_day.values()), estimates)

        mmre_with_dates = {}
        for index, day in enumerate(cumulated_completed_task_per_day.keys()):
            mmre_with_dates[day] = mmre[index]

        all_sets_to_plot[f'{n} days forecast'] = estimates_with_dates
        mmre_to_plot[f'{n} days forecast'] = mmre_with_dates

    project_graph_file = Path(sys.argv[1]).parent / "graph_actual_work_and_estimates"
    show_graph(project_graph_file, all_sets_to_plot)

    mmre_graph_file = Path(sys.argv[1]).parent / "graph_mmre"
    show_graph(mmre_graph_file, mmre_to_plot)


main()
