import pytest
from mmre import compute_all_mmre, compute_mmre, compute_signed_mmre


class TestMRE:
    @pytest.mark.parametrize("actual, estimated, expected_result", [
        (1.0, 1.0, 0.0),
        (100.0, 100.0, 0.0),
        (100.0, 200.0, 1.0),
        (200.0, 100.0, 0.5),
        (100.0, 400.0, 3.0),
    ])
    def test_mmre_formula(self, actual, estimated, expected_result):
        assert compute_mmre(actual, estimated) == expected_result

    @pytest.mark.parametrize("actual, estimated, expected_result", [
        (1.0, 1.0, 0.0),
        (100.0, 100.0, 0.0),
        (100.0, 200.0, 1.0),
        (200.0, 100.0, -0.5),
        (100.0, 400.0, 3.0),
    ])
    def test_signed_mmre_formula(self, actual, estimated, expected_result):
        assert compute_signed_mmre(actual, estimated) == expected_result

    def test_perfect_forecast(self):
        actual_project_cumulative_flow = [1, 2, 2, 4, 5]
        forecast_project_cumulative_flow = [1, 2, 2, 2, 10]

        actual_all_mmre = compute_all_mmre(actual_project_cumulative_flow, forecast_project_cumulative_flow)
        assert actual_all_mmre == [0.0, 0.0, 0.0, 0.5, 1.0]
