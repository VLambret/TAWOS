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
        self.resolution= issue_data['Resolution']
        self.resolution_date = issue_data['Resolution_Date']


class Project:
    def __init__(self, data):
        self.id = data["ID"]
        self.name = data["Name"]

    def get_issues(self) -> list[Issue]:
        query = f"""
            SELECT *
            FROM Issue
            WHERE Issue.Project_ID = {self.id} AND Issue.Status = "Done" and Issue.Resolution = "Complete";
        """

        return [Issue(i) for i in (db.query(query))]


class Tawos:
    def __init__(self):
        pass

    def get_projects(self) -> list[Project]:
        query = "Select * from Project;"
        return [Project(data) for data in db.query(query)]

    def get_tables(self):
        query = "SHOW TABLES;"
        return db.query(query)
