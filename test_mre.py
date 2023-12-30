from mre import compute_all_mre, compute_mre


class TestMRE:
    def test_mre_formula(self):
        assert compute_mre(1.0, 1.0) == 1.0

    def test_perfect_forecast(self):
        actual_project_cumulative_flow = [1, 2, 3, 4, 5]
        forecast_project_cumulative_flow = [1, 2, 3, 4, 5]

        actual_all_mre = compute_all_mre(actual_project_cumulative_flow, forecast_project_cumulative_flow)
        assert actual_all_mre == [1.0, 1.0, 1.0, 1.0, 1.0]



