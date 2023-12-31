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
