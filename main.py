import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

from dateutil.relativedelta import relativedelta

from tawos import Tawos


def count_occurrences(dates: list[datetime]) -> dict[datetime:int]:
    dates = [date.strftime("%Y-%m-%d") for date in dates]

    counter = dict(Counter(dates))

    result = {}
    issue_closed = 0
    for k in sorted(counter.keys()):
        issue_closed += counter[k]
        result[k] = issue_closed

    return {datetime.strptime(d, "%Y-%m-%d"): v for d, v in result.items()}


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


def no_estimates_projection(progress: dict[datetime:int]) -> dict[datetime:int]:
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


def show_graph(progress, estimates):
    progress_dates = list(progress.keys())
    progress_values = list(progress.values())

    estimates_dates = list(estimates.keys())
    estimates_values = list(estimates.values())

    plt.plot(progress_dates, progress_values)
    plt.plot(estimates_dates, estimates_values, marker='o')

    plt.xlabel('Date')
    plt.ylabel('# of Completed issues')
    plt.title('Completed issues over time')

    plt.show()


def main():
    projects = Tawos().get_projects()

    issues = projects[0].get_issues()
    resolutions_dates = [i.resolution_date for i in issues]
    progress = count_occurrences(resolutions_dates)
    estimates = no_estimates_projection(progress)
    show_graph(progress, estimates)
    print(issues[0])


main()
