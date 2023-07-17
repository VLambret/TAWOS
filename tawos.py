from collections import Counter

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
        self.resolution_date = self.get_resolution_date(issue_data)

    def get_resolution_date(self, issue_data):
        if issue_data['Resolution_Date']:
            return issue_data['Resolution_Date']
        else:
            return issue_data['Last_Updated']

    def get_done_status(self, status):
        return status in ["Done", "Closed", "Resolved", "Accepted"]


class Project:
    def __init__(self, data):
        self.id = data["ID"]
        self.name = data["Name"]

        query = f"""
            SELECT *
            FROM Issue
            WHERE Issue.Project_ID = {self.id};
        """
        self.issues = [Issue(i) for i in (db.query(query))]
        self.print_stats()

    def get_issues(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.is_done]

    def print_stats(self):
        print(f"Issues stats:")
        status_stat = dict(Counter([i.status for i in self.issues]))
        print(status_stat)


class Tawos:
    def __init__(self):
        pass

    def get_projects(self) -> list[Project]:
        query = "Select * from Project;"
        return [Project(data) for data in db.query(query)]

    def get_tables(self):
        query = "SHOW TABLES;"
        return db.query(query)
