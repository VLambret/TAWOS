import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

import mysql.connector


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


def count_occurrences(dates: list[datetime]):
    dates = [date.strftime("%Y-%m-%d") for date in dates]

    counter = dict(Counter(dates))

    result = {}
    issue_closed = 0
    for k in sorted(counter.keys()):
        issue_closed += counter[k]
        result[k] = issue_closed

    return {datetime.strptime(d, "%Y-%m-%d"):v for d,v in result.items()}

def show_graph(data):
    dates = list(data.keys())
    values = list(data.values())

    date_labels = dates

    plt.plot(date_labels, values)

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
show_graph(progress)

print(issues[0])