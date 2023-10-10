import unittest

from TeamProgress import TeamProgress


class TeamProgressTest(unittest.TestCase):
    def test_finished_ticket_dates_are_YYYY_MM_DD_with_dashes_separators(self):
        finished_ticket_dates = [
            "2010-01-01",
        ]

        progress = TeamProgress(finished_ticket_dates)
        self.assertEqual(1, progress.ticket_closed_at("2010-01-01"))  # add assertion here


if __name__ == '__main__':
    unittest.main()
