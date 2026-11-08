"""Quality gate: a model that is too inaccurate must not be released."""
import json

PASS_MARK = 0.1.0  # USD


def test_quality_gate():
    with open("metrics.json") as f:
        mae = json.load(f)["mae"]
    assert mae < PASS_MARK, f"MAE {mae} is not below the pass mark {PASS_MARK}"
