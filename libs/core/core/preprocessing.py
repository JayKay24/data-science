import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize DataFrame column names to lowercase snake_case."""
    df_copy = df.copy()
    df_copy.columns = (
        df_copy.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )
    return df_copy
