#! /usr/bin/python3

from tawos import Tawos


def main():
    projects = Tawos().get_projects()
    for project in projects:
        project.save_dates_on_disk()


main()
