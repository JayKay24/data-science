import numpy as np
from core.metrics import calculate_classification_metrics


def test_calculate_classification_metrics() -> None:
    y_true = np.array([1, 0, 1, 1, 0, 1])
    y_pred = np.array([1, 0, 1, 0, 0, 1])

    metrics = calculate_classification_metrics(y_true, y_pred)

    assert metrics["accuracy"] > 0.8
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
