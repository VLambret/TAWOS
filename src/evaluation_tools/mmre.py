# MMRE: Mean Magnitude of Relative Error
def compute_signed_mmre(actual: float, estimated: float) -> float:
    if estimated == actual:
        return 0
    return (estimated - actual) / actual


def compute_mmre(actual: float, estimated: float) -> float:
    # MMRE: Absolute Value((Actual result - Estimated result) / Actual Result)
    return abs(compute_signed_mmre(actual, estimated))

