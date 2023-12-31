from datetime import date


class TestDatedValues:
    def test_can_be_compared(self):
        task_end_dates = {
            date(2023, 1, 3): 42,
            date(2023, 1, 3): 43
        }

        values1= None
