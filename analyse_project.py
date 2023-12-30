#! /usr/bin/python3
import sys
import matplotlib
import matplotlib.figure
from datetime import date, datetime
from pathlib import Path

from cumulative_flow import CumulativeFlow


def show_graph(filename: Path, real_progress: dict[date, float], estimates: dict[date, float]):
    progress_dates = list(real_progress.keys())
    progress_values = list(real_progress.values())

    estimates_dates = list(estimates.keys())
    estimates_values = list(estimates.values())

    figure = matplotlib.figure.Figure(figsize=(8, 6))

    figure_axis = figure.add_subplot()
    figure.suptitle(f'{filename} - Completed issues over time')

    figure_axis.set_xlabel('Date')
    figure_axis.set_ylabel('# of Completed issues')

    figure_axis.plot(progress_dates, progress_values)
    figure_axis.plot(estimates_dates, estimates_values, marker='o')
    figure.savefig(filename, dpi=300)


def load_dates_from(project_csv: Path) -> list[date]:
    with project_csv.open('r') as f:
        return [datetime.strptime(d.strip(), "%Y-%m-%d").date() for d in f.readlines()]


def main():
    project_csv = Path(sys.argv[1])

    dates = load_dates_from(project_csv)
    project_activity = CumulativeFlow(dates)

    cumulated_completed_task_per_day = project_activity.total_closed_task_per_day

    project_graph_file = Path(sys.argv[1]).parent / "graph_actual_work_and_estimates"
    show_graph(project_graph_file, cumulated_completed_task_per_day, {})


main()
