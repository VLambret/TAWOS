import pytest
from mmre import compute_mmre, compute_signed_mmre


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
