from churn_prediction.features import prepare_synthetic_data


def test_prepare_synthetic_data():
    X, y = prepare_synthetic_data(50)
    assert len(X) == 50
    assert len(y) == 50
    assert "monthly_charges" in X.columns
    assert "tenure_months" in X.columns
    assert "contract_type" in X.columns
