from collections import Counter
from datetime import datetime

import matplotlib.figure
from dateutil.relativedelta import relativedelta

from tawos import Tawos


class IssuesGroupedByDay:
    def __init__(self, dates: list[datetime]):
        dates = [date.strftime("%Y-%m-%d") for date in dates]

        counter = dict(Counter(dates))

        issue_closed = 0
        self.grouped_issues = {}
        for k in sorted(counter.keys()):
            issue_closed += counter[k]
            self.grouped_issues[k] = issue_closed

        self.grouped_issues = {datetime.strptime(d, "%Y-%m-%d"): v for d, v in self.grouped_issues.items()}


def keep_last_value_at_fixed_intervals(progress, estimation_interval_in_month) -> dict[datetime:int]:
    intervals = {}
    dates = sorted(progress.keys())

    min_date = min(dates)
    for date in dates:
        delta = relativedelta(date, min_date)
        months = (delta.years * 12 + delta.months)
        index = int(months / estimation_interval_in_month)

        if index not in intervals:
            intervals[index] = []
        intervals[index].append(progress[date])

    return {k: max(v) for k, v in intervals.items()}


def compute_first_rought_estimate(progress, estimation_interval_in_month):
    dates = sorted(progress.keys())
    min_date = min(dates)
    months_before_first_evaluation = 3
    first_month_of_work = min_date + relativedelta(months=months_before_first_evaluation)

    def is_in_first_month(d):
        return d < first_month_of_work

    last_date_in_first_month = max(filter(is_in_first_month, dates))

    # We wait for 1 month, and then we project to the end of the estimation interval
    return progress[last_date_in_first_month] / months_before_first_evaluation * estimation_interval_in_month


def no_estimates_projection(grouped_issues: IssuesGroupedByDay) -> dict[datetime:int]:
    progress: dict[datetime:int] = grouped_issues.grouped_issues
    estimation_interval_in_month = 6

    grouped = keep_last_value_at_fixed_intervals(progress, estimation_interval_in_month)

    dates = sorted(progress.keys())
    min_date = min(dates)

    # We start at origin in order to print the full graph
    estimates = {min_date: 0}

    # To draw the start of estimation line, first we draw first date when we're estimating.
    estimation_start = min_date + relativedelta(months=estimation_interval_in_month)

    first_rought_estimate = compute_first_rought_estimate(progress, estimation_interval_in_month)
    estimates[estimation_start] = first_rought_estimate

    previous_value = 0
    for index, value in grouped.items():
        d = min_date + relativedelta(months=(index + 2) * estimation_interval_in_month)
        issues_closed_last_6_month = value - previous_value
        v = value + issues_closed_last_6_month
        previous_value = value
        estimates[d] = v

    return estimates


def show_graph(project_name: str, real_progress, estimates):
    progress_dates = list(real_progress.keys())
    progress_values = list(real_progress.values())

    estimates_dates = list(estimates.keys())
    estimates_values = list(estimates.values())

    figure = matplotlib.figure.Figure(figsize=(8, 6))

    figure_axis = figure.add_subplot()
    figure.suptitle(f'{project_name} - Completed issues over time')

    figure_axis.set_xlabel('Date')
    figure_axis.set_ylabel('# of Completed issues')

    figure_axis.plot(progress_dates, progress_values)
    figure_axis.plot(estimates_dates, estimates_values, marker='o')
    figure.savefig(f"{project_name.replace(' ', '_')}.png", dpi=300)


def plot_real_progress_and_estimates(project):
    issues = project.get_issues()
    resolutions_dates = [i.resolution_date for i in issues]
    progress = IssuesGroupedByDay(resolutions_dates)
    estimates = no_estimates_projection(progress)
    show_graph(project.name, progress.grouped_issues, estimates)


def main():
    projects = Tawos().get_projects()
    for project in projects:
        print(f"Analysing project {project.name}")
        try:
            plot_real_progress_and_estimates(project)
        except:
            print(f"ERROR ON PROJECT {project.name}")


main()
