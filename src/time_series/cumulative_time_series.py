from dataclasses import dataclass
from datetime import date
from typing import Dict

from evaluation_tools.mmre import compute_signed_mmre, compute_mmre

DatedValuesType = Dict[date, float | int]


@dataclass
class DatedValue:
    date: date
    value: int | float


class CumulativeTimeSeries:

    def __init__(self, values: DatedValuesType):
        self.values: list[DatedValue] = [DatedValue(d, v) for d, v in values.items()]

    def __getitem__(self, day_number):
        return self.values[day_number - 1]

    def __eq__(self, other):
        if not isinstance(other, CumulativeTimeSeries):
            return False

        return self.values == other.values

    def get_dates(self) -> list[date]:
        return [v.date for v in self.values]

    def get_values(self) -> list[int | float]:
        return [v.value for v in self.values]

    def compute_mmre_compared_to_reference(self, reference: "CumulativeTimeSeries") -> "CumulativeTimeSeries":
        r = {}
        for index, v in enumerate(self.values):
            actual = reference.values[index].value
            compared = v.value
            r[v.date] = compute_mmre(actual, compared)
        return CumulativeTimeSeries(r)

    def compute_signed_mmre_compared_to_reference(self, reference: "CumulativeTimeSeries") -> "CumulativeTimeSeries":
        r = {}
        for index, v in enumerate(self.values):
            actual = reference.values[index].value
            compared = v.value
            r[v.date] = compute_signed_mmre(actual, compared)
        return CumulativeTimeSeries(r)

    def compute_completed_task_last_period(self, period_in_days: int) -> "CumulativeTimeSeries":
        r = {}
        for index, v in enumerate(self.values):
            period_start = index - period_in_days
            start_value: int | float
            if period_start < 0:
                start_value = 0
            else:
                start_value = self.values[period_start].value
            r[v.date] = v.value - start_value
        return CumulativeTimeSeries(r)
