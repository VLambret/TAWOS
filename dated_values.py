from datetime import date

DatedValuesType = dict[date, [float | int]]


class DatedValues:

    def __init__(self, values: DatedValuesType):
        self.values = values

    def __eq__(self, other):
        if not isinstance(other, DatedValues):
            return False

        return self.values == other.values

