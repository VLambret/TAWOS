from datetime import date

from cumulative_flow import get_cumulative_flow


class TestCumulativeFlow:
    def test_cumulative_flow(self):
        task_end_dates = [
            date(2023, 1, 3),
            date(2023, 1, 1),
        ]
        flow = get_cumulative_flow(task_end_dates)

        expected: dict[date: int] = {
            date(2023, 1, 1): 1,
            date(2023, 1, 2): 1,
            date(2023, 1, 3): 2,
        }

        assert expected == flow




