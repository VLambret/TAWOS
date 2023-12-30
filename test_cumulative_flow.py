from datetime import date

from cumulative_flow import CumulativeFlow


class TestCumulativeFlow:
    def test_cumulative_flow(self):
        task_end_dates = [
            date(2023, 1, 3),
            date(2023, 1, 1),
        ]
        flow = CumulativeFlow(task_end_dates).total_closed_task_per_day

        expected: dict[date: int] = {
            date(2023, 1, 1): 1,
            date(2023, 1, 2): 1,
            date(2023, 1, 3): 2,
        }

        assert expected == flow




