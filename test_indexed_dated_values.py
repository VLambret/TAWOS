from datetime import date

from indexed_dated_values import IndexedDatedValues, DatedValue


class TestDatedValues:
    def test_can_be_compared(self):
        assert DatedValue(date(2023, 1, 3), 42) == DatedValue(date(2023, 1, 3), 42)
        assert DatedValue(date(2023, 1, 3), 42) != DatedValue(date(2023, 1, 3), 43)


class TestIndexedDatedValues:
    data1 = {
        date(2023, 1, 3): 1,
        date(2023, 1, 4): 2
    }

    data2 = {
        date(2023, 1, 5): 3,
        date(2023, 1, 6): 4
    }

    values1 = IndexedDatedValues(data1)
    values2 = IndexedDatedValues(data1)
    values3 = IndexedDatedValues(data2)

    def test_can_be_compared(self):

        assert self.values1 == self.values2
        assert self.values1 != self.values3

    def test_can_access_element_from_index(self):
        assert self.values1[1] == DatedValue(date(2023, 1, 3), 1)

