#! /usr/bin/python3
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict

from evaluation_tools.metrics import compute_mmre, compute_signed_mmre, compute_mmre_quality, compute_all_risk_being_late
from graph import save_as_graph_old, save_as_graph
from time_series.normalized_time_series import NormalizedTimeSeries
from time_series.cumulative_time_series import CumulativeTimeSeries
from forecasts.no_estimate_forecast import NoEstimateForecast


class Project:
    def __init__(self, dates_in_csv_file: str):
        dates_in_csv_file_path: Path = Path(dates_in_csv_file)
        dates = load_dates_from(dates_in_csv_file_path)

        self.folder: Path = dates_in_csv_file_path.parent
        self.name = dates_in_csv_file_path.name.replace('_', " ").removesuffix(".csv")
        self.activity = NormalizedTimeSeries(dates)
        self.filtered_activity = NormalizedTimeSeries(dates, filter=True)


def load_dates_from(project_csv: Path) -> list[date]:
    with project_csv.open('r') as f:
        return [datetime.strptime(d.strip(), "%Y-%m-%d").date() for d in f.readlines()]


def save_as_json_old(project: Project, mmre_quality: dict[str, CumulativeTimeSeries], file_name) -> None:
    result: dict = {project.name: {
        v.date :v.value
        for v in mmre_quality['MMRE quality'].values
    }}
    with open(project.folder / file_name, 'w') as json_file:
        json.dump(result, json_file, indent=4, default=str)

def save_as_json(project: Project, data: Dict[str, Dict[int, float]], file_name) -> None:
    with open(project.folder / file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=str)


def main() -> None:
    project = Project(sys.argv[1])

    ################################################################################
    # REAL TOTAL CUMULATED CLOSED TASKS
    ################################################################################

    unfiltered_real_total_completed_tasks_per_day: CumulativeTimeSeries = project.activity.cumulated_completed_tasks
    filtered_real_total_completed_tasks_per_day: CumulativeTimeSeries = project.filtered_activity.cumulated_completed_tasks
    real_total_completed_tasks_per_day = filtered_real_total_completed_tasks_per_day


    unfiltered_reality: dict[str, CumulativeTimeSeries] = {
        "Unfiltered": unfiltered_real_total_completed_tasks_per_day,
        "Filtered": filtered_real_total_completed_tasks_per_day
    }
    save_as_graph_old(project,
                  "real activity ",
                  "Date",
                  'total completed issues',
                      unfiltered_reality)

    reality = {
        "Reality": filtered_real_total_completed_tasks_per_day
    }

    ################################################################################
    # USING TOTAL CUMULATED COMPLETED TASKS
    ################################################################################

    all_total_completed_tasks_per_day_estimates = get_all_total_completed_tasks_per_day_estimates(project.filtered_activity)

    all_estimates_to_plot: dict[str, CumulativeTimeSeries] = {"Reality": real_total_completed_tasks_per_day}
    for n in [180, 360]:
        all_estimates_to_plot[f'{n} days'] = all_total_completed_tasks_per_day_estimates[n]

    save_as_graph_old(project,
                  "cumulated completed task forecasts",
                  "Date",
                  'total completed issues',
                      all_estimates_to_plot)

    # Signed MMRE
    signed_mmre_to_plot = compute_signed_mmre(real_total_completed_tasks_per_day,
                                              all_estimates_to_plot)
    save_as_graph_old(project,
                  "cumulated completed task forecasts signed MMRE",
                  "Date",
                  'Signed MMRE',
                      signed_mmre_to_plot)

    # MMRE
    mmre_to_plot = compute_mmre(real_total_completed_tasks_per_day,
                                all_estimates_to_plot)
    save_as_graph_old(project,
                  "cumulated completed task forecasts MMRE",
                  "Date",
                  'MMRE',
                      mmre_to_plot)

    # MMRE Quality
    mmre_quality = compute_mmre_quality(all_total_completed_tasks_per_day_estimates,
                                        real_total_completed_tasks_per_day)

    save_as_graph_old(project,
                  "Average MMRE for each period",
                  "Date",
                  'Average MMRE',
                      mmre_quality)

    save_as_json_old(project, mmre_quality, 'mmre_quality.json')

    ## Risk being late
    #risk_being_late = compute_all_risk_being_late(all_total_completed_tasks_per_day_estimates,
    #                                              real_total_completed_tasks_per_day)

    #save_as_graph(project,
    #              "Risk being late",
    #              "Date",
    #              'Average MMRE',
    #                  risk_being_late)

    #save_as_json(project, risk_being_late, 'risk_being_late.json')


def get_all_total_completed_tasks_per_day_estimates(project_activity):
    estimate_periods = [1, 5, 10, 20, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 720]
    all_estimates: dict[int, CumulativeTimeSeries] = {
        period: NoEstimateForecast(project_activity, period, period).forecast_for_all_days()
        for period in estimate_periods
    }
    return all_estimates


if __name__ == "__main__":
    main()
