from typing import Dict

import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

import mysql.connector
from dateutil.relativedelta import relativedelta


class Tawos:
    def __init__(self):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="tawos",
            password="tawospass",
            database="tawos",
        )

        self.cursor = self.connexion.cursor(dictionary=True)

    def get_tables(self):
        query = "SHOW TABLES;"
        return self.query(query)

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_issues(self):
        query = """
            Select Issue.ID, Issue.Creation_Date, Issue.Last_Updated, Issue.Resolution_Date , Issue.Story_Point, Issue.Story_Point_Changed_After_Estimation
            from Issue
            WHERE Issue.Project_ID = 1 AND Issue.Status = "Done" and Issue.Resolution = "Complete";
        """

        return self.query(query)


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


def no_estimates_projection(progress: dict[datetime:int]) -> dict[datetime:int]:
    estimation_interval_in_month = 6

    grouped = keep_last_value_at_fixed_intervals(progress, estimation_interval_in_month)

    dates = sorted(progress.keys())
    min_date = min(dates)

    # To draw the start of estimation line, first we draw first date when we're estimating.
    estimation_start = min_date + relativedelta(months=estimation_interval_in_month)
    estimates = {estimation_start: min(grouped.values())}
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


tawos = Tawos()
tables = tawos.get_tables()

for table in tables:
    print(table)

issues = tawos.get_issues()
resolutions_dates = [i['Resolution_Date'] for i in issues]
progress = count_occurrences(resolutions_dates)
estimates = no_estimates_projection(progress)
show_graph(progress, estimates)

print(issues[0])
