from statistics import mean
from typing import Dict

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


def compute_risk_being_late(param) -> float:
    assert False
    return 12.7


def compute_all_risk_being_late(all_total_completed_tasks_per_day_estimates, real_total_completed_tasks_per_day) -> Dict[str, Dict[int, float]]:

    all_signed_mmre = compute_signed_mmre(real_total_completed_tasks_per_day, all_total_completed_tasks_per_day_estimates)

    risk_being_late = {"Risk being late":
        {
            period: compute_risk_being_late(values.compute_mmre_compared_to_reference(real_total_completed_tasks_per_day).get_values())
            for period, values in all_signed_mmre.items()
        }
    }
    return risk_being_late
