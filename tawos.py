from collections import Counter
from datetime import datetime
from pathlib import Path

import mysql.connector


class DB:
    def __init__(self):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="tawos",
            password="tawospass",
            database="tawos",
        )

        self.cursor = self.connexion.cursor(dictionary=True)

    def query(self, sql_query):
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()


db = DB()


class Issue:
    def __init__(self, issue_data):
        self.status = issue_data['Status']
        self.resolution = issue_data['Resolution']
        self.data = issue_data

        self.is_done: bool = self.get_done_status(issue_data['Status'])
        self.resolution_date: datetime = self.get_resolution_date(issue_data)

    def get_resolution_date(self, issue_data):
        if issue_data['Resolution_Date']:
            return issue_data['Resolution_Date']
        else:
            return issue_data['Last_Updated']

    def get_done_status(self, status):
        # List determined using stats on all issue status
        return status in ["Done", "Closed", "Resolved", "Complete"]


class Project:
    def __init__(self, data):
        self.id = data["ID"]
        self.name = data["Name"]
        self.sanitized_name = self.name.replace(' ', '_')

        query = f"""
            SELECT *
            FROM Issue
            WHERE Issue.Project_ID = {self.id};
        """
        self.issues: list[Issue] = [Issue(i) for i in (db.query(query))]
        self.print_stats()

    def get_issues(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.is_done]

    def get_project_folder(self) -> Path:
        p = Path(f"projects/{self.sanitized_name}")
        p.mkdir(parents=True, exist_ok=True)
        return p

    def save_dates_on_disk(self):
        completion_dates = [issue.resolution_date.strftime("%Y-%m-%d") for issue in self.issues if issue.is_done]
        with open(self.get_project_folder() / "input.csv", 'w') as f:
            for d in completion_dates:
                f.write(f"{d}\n")

    def print_stats(self):
        print(f"Issues stats:")
        status_stat = dict(Counter([i.status for i in self.issues]))
        print(status_stat)


class Tawos:
    def __init__(self):
        pass

    def show_status_stats_on_all_projects(self):
        query = """
            SELECT Status, COUNT(*) AS Count
            FROM Issue
            GROUP BY Status;
        """
        status_stats = db.query(query)
        for stat in status_stats:
            print(f'{stat["Count"]}:{stat["Status"]}')

    def get_projects(self) -> list[Project]:
        query = "Select * from Project;"
        return [Project(data) for data in db.query(query)]

    def get_tables(self):
        query = "SHOW TABLES;"
        return db.query(query)
