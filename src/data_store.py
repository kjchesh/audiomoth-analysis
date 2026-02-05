"""Handle data storage and retrieval."""

from src.normaliser import clean_column_names
import pandas as pd
from pathlib import Path


def get_excel_sheets(excel_path: Path) -> dict[str, pd.DataFrame]:
    """Read all sheets from the given Excel file into a dictionary of
    DataFrames. Each DataFrame will have cleaned column names.
    """
    sheets = pd.read_excel(excel_path, sheet_name=None)
    for name, df in sheets.items():
        new_df = clean_column_names(df)
        sheets[name] = new_df
    return sheets


def save_dataframes_to_csv(
    dataframes: dict[str, pd.DataFrame], output_dir: Path
) -> None:
    """Save each DataFrame in the given dictionary to a CSV file in the specified output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, df in dataframes.items():
        csv_path = output_dir / f"{name}.csv"
        df.to_csv(csv_path, index=False)
