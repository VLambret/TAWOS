from time_series.cumulative_time_series import CumulativeTimeSeries


def compute_mmre(reference: CumulativeTimeSeries, estimates: dict[str, CumulativeTimeSeries]) -> dict[str, CumulativeTimeSeries]:
    return {
        tag: estimate.compute_mmre_compared_to_reference(reference) for tag, estimate
        in
        estimates.items()
    }


def compute_signed_mmre(reference, estimates):
    return {
        tag: estimate.compute_signed_mmre_compared_to_reference(reference) for tag, estimate
        in
        estimates.items()
    }
