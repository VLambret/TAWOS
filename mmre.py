
# MMRE: Mean Magnitude of Relative Error
def compute_mmre(actual: float, estimated: float) -> float:
    # MMRE: Absolute Value((Actual result - Estimated result) / Actual Result)
    return abs(actual - estimated) / actual

def compute_all_mmre(actuals: list[float], estimateds: list[float]) -> list[float]:
    return [compute_mmre(actuals[index], estimateds[index]) for index, _ in enumerate(actuals)]


