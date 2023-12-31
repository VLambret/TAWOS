from datetime import date

from dated_values import DatedValues


class TestDatedValues:
    data1 = {
        date(2023, 1, 3): 42,
        date(2023, 1, 3): 43
    }

    data2 = {
        date(2023, 1, 3): 52,
        date(2023, 1, 3): 53
    }

    values1 = DatedValues(data1)
    values2 = DatedValues(data1)
    values3 = DatedValues(data2)

    def test_can_be_compared(self):
        assert self.values1 == self.values2
        assert self.values1 != self.values3
