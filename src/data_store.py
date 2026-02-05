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
