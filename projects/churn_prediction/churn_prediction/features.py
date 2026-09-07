from typing import Tuple
import numpy as np
import pandas as pd
from core.preprocessing import clean_column_names


def prepare_synthetic_data(n_samples: int = 200) -> Tuple[pd.DataFrame, pd.Series]:
    """Generate and preprocess a synthetic customer churn dataset."""
    np.random.seed(42)
    data = {
        "Monthly Charges": np.random.uniform(20.0, 120.0, n_samples),
        "Tenure Months": np.random.randint(1, 72, n_samples),
        "Contract Type": np.random.choice([0, 1, 2], n_samples),
    }
    df = pd.DataFrame(data)
    df = clean_column_names(df)

    # Simple churn propensity heuristic
    churn_prob = 1 / (
        1 + np.exp(-(0.03 * df["monthly_charges"] - 0.05 * df["tenure_months"]))
    )
    churn = (np.random.uniform(0, 1, n_samples) < churn_prob).astype(int)
    return df, pd.Series(churn, name="churn")
