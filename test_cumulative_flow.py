from datetime import date

from cumulative_flow import CumulativeFlow


class TestCumulativeFlow:
    def test_cumulative_flow_compute_total_closed_task_on_a_day_from_task_end_dates(self):
        task_end_dates = [
            date(2023, 1, 3),
            date(2023, 1, 3),
            date(2023, 1, 5),
            date(2023, 1, 1),
        ]
        flow = CumulativeFlow(task_end_dates).total_closed_task_per_day

        expected: dict[date: int] = {
            date(2023, 1, 1): 1,
            date(2023, 1, 2): 1,
            date(2023, 1, 3): 3,
            date(2023, 1, 4): 3,
            date(2023, 1, 5): 4,
        }

        assert flow == expected

    def test_total_task_can_also_be_obtained_with_a_day_number(self):
        task_end_dates = [
            date(2023, 1, 2),
            date(2023, 1, 2),
            date(2023, 1, 3),
            date(2023, 1, 1),
        ]
        assert CumulativeFlow(task_end_dates).get_total_closed_task_on_day(2) == 3

    def test_can_give_total_tasks_outside_of_project_interval(self):
        task_end_dates = [
            date(2023, 1, 10),
            date(2023, 1, 11),
            date(2023, 1, 12),
        ]
        CumulativeFlow(task_end_dates).get_total_closed_task_on_day(1)
        CumulativeFlow(task_end_dates).get_total_closed_task_on_day(3)

        assert CumulativeFlow(task_end_dates).get_total_closed_task_on_day(0) == 0
        assert CumulativeFlow(task_end_dates).get_total_closed_task_on_day(4) == 3
