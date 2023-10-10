import collections


class TeamProgress:

    def __init__(self, finished_ticket_dates: list):
        self.finished_tickets = collections.Counter(finished_ticket_dates)

    def ticket_closed_at(self, date):
        return self.finished_tickets[date]
