# MMRE: Mean Magnitude of Relative Error
def compute_signed_mmre(actual: float, estimated: float) -> float:
    return (estimated - actual) / actual


def compute_mmre(actual: float, estimated: float) -> float:
    # MMRE: Absolute Value((Actual result - Estimated result) / Actual Result)
    return abs(compute_signed_mmre(actual, estimated))


def compute_all_mmre(actuals: list[float], estimateds: list[float]) -> list[float]:
    return [compute_mmre(actuals[index], estimateds[index]) for index, _ in enumerate(actuals)]


def compute_all_signed_mmre(actuals: list[float], estimateds: list[float]) -> list[float]:
    return [compute_signed_mmre(actuals[index], estimateds[index]) for index, _ in enumerate(actuals)]
