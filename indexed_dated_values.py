from dataclasses import dataclass
from datetime import date

DatedValuesType = dict[date, [float | int]]


@dataclass
class DatedValue:
    date: date
    value: [int | float]


class IndexedDatedValues:

    def __init__(self, values: DatedValuesType):
        self.values: list[DatedValue] = [DatedValue(d, v) for d, v in values.items()]

    def __getitem__(self, day_number):
        return self.values[day_number - 1]

    def __eq__(self, other):
        if not isinstance(other, IndexedDatedValues):
            return False

        return self.values == other.values

    def get_dates(self) -> list[date]:
        return [v.date for v in self.values]

    def get_values(self) -> list[int | float]:
        return [v.value for v in self.values]

    def compute_signed_mmre_compared_to(self, actual: "IndexedDatedValues") -> "IndexedDatedValues":
        r = {}
        for index, v in enumerate(self.values):
            r[v.date] = 0.0
        return IndexedDatedValues(r)
