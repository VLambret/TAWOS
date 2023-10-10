import unittest

from TeamProgress import TeamProgress


class TeamProgressTest(unittest.TestCase):
    def test_finished_ticket_dates_are_YYYY_MM_DD_with_dashes_separators(self):
        finished_ticket_dates = [
            "2010-01-01",
        ]

        progress = TeamProgress(finished_ticket_dates)
        self.assertEqual(1, progress.ticket_closed_at("2010-01-01"))  # add assertion here

    def test_progress_count_all_tickets_closed_on_a_day(self):
        finished_ticket_dates = [
            "2010-01-03",
            "2010-01-02",
            "2010-01-03",
        ]

        progress = TeamProgress(finished_ticket_dates)
        self.assertEqual(1, progress.ticket_closed_at("2010-01-02"))  # add assertion here
        self.assertEqual(2, progress.ticket_closed_at("2010-01-03"))  # add assertion here

    def test_zero_is_returned_when_no_tickets_are_closed_that_day(self):
        finished_ticket_dates = [
            "2010-01-04",
        ]

        progress = TeamProgress(finished_ticket_dates)
        self.assertEqual(0, progress.ticket_closed_at("2010-01-05"))  # add assertion here


if __name__ == '__main__':
    unittest.main()
