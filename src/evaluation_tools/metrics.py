from statistics import mean

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


def compute_mmre_quality(all_total_completed_tasks_per_day_estimates, real_total_completed_tasks_per_day):
    mmre_quality = {"MMRE quality": CumulativeTimeSeries(
        {
            period: mean(values.compute_mmre_compared_to_reference(real_total_completed_tasks_per_day).get_values())
            for period, values in all_total_completed_tasks_per_day_estimates.items()
        })
    }
    return mmre_quality
