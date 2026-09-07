import numpy as np
from sklearn.linear_model import LogisticRegression
from core.metrics import calculate_classification_metrics
from churn_prediction.features import prepare_synthetic_data


def train_model() -> None:
    X, y = prepare_synthetic_data(300)
    model = LogisticRegression()
    model.fit(X, y)

    preds = model.predict(X)
    metrics = calculate_classification_metrics(y.to_numpy(), np.array(preds))
    print(f"Model trained successfully. Train metrics: {metrics}")


def get_trained_model() -> LogisticRegression:
    X, y = prepare_synthetic_data(300)
    model = LogisticRegression()
    model.fit(X, y)
    return model


if __name__ == "__main__":
    train_model()
