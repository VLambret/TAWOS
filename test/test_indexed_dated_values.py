from datetime import date

from src.indexed_dated_values import IndexedDatedValues, DatedValue


class TestIndexedDatedValues:
    data1 = {
        date(2023, 1, 3): 100.0,
        date(2023, 1, 4): 200.0
    }

    data2 = {
        date(2023, 1, 3): 200.0,
        date(2023, 1, 4): 100.0
    }

    values1 = IndexedDatedValues(data1)
    values2 = IndexedDatedValues(data1)
    values3 = IndexedDatedValues(data2)

    def test_can_be_compared(self):
        assert self.values1 == self.values2
        assert self.values1 != self.values3

    def test_can_access_element_from_index(self):
        assert self.values1[1] == DatedValue(date(2023, 1, 3), 100.0)

    def test_compute_signed_mmre_ideal(self):
        mmre = self.values1.compute_signed_mmre_compared_to_reference(self.values1)
        expected = IndexedDatedValues({date(2023, 1, 3): 0.0,
                                       date(2023, 1, 4): 0.0
                                       })
        assert mmre.values == expected.values

    def test_compute_signed_mmre_with_difference(self):
        reference = IndexedDatedValues({
            date(2023, 1, 3): 100.0,
            date(2023, 1, 4): 150.0,
        })

        estimation = IndexedDatedValues({
            date(2023, 1, 3): 200.0,
            date(2023, 1, 4): 75.0,
        })
        mmre = estimation.compute_signed_mmre_compared_to_reference(reference)

        expected = IndexedDatedValues({
            date(2023, 1, 3): 1.0,
            date(2023, 1, 4): -0.5,
        })
        assert mmre.values == expected.values

    def test_group_diff_by_period(self):
        increasing_values_each_day = IndexedDatedValues({
            date(2023, 1, 1): 1.0,
            date(2023, 1, 2): 2.0,
            date(2023, 1, 3): 3.0,
            date(2023, 1, 4): 4.0,
            date(2023, 1, 5): 5.0,
            date(2023, 1, 6): 6.0,
            date(2023, 1, 7): 8.0,
        })

        grouped_diff = increasing_values_each_day.compute_completed_task_last_period(3)

        expected = IndexedDatedValues({
            date(2023, 1, 1): 1.0,
            date(2023, 1, 2): 2.0,
            date(2023, 1, 3): 3.0,
            date(2023, 1, 4): 3.0,
            date(2023, 1, 5): 3.0,
            date(2023, 1, 6): 3.0,
            date(2023, 1, 7): 4.0,
        })

        assert grouped_diff.values == expected.values
