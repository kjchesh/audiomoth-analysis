"""The audiomoth data needs some basic cleaning to have consistent column names and types."""

import pandas as pd
from pathlib import Path
import datetime as dt


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataframe to have consistent column names and types."""
    # Lowercase/underscore column names
    df = df.rename(
        columns={
            c: c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
            for c in df.columns
        }
    )
    return df


def combine_date_and_time(
    df: pd.DataFrame,
    date_col: str,
    time_col: str,
    output_col: str = "timestamp",
) -> pd.DataFrame:
    """
    Combine a date column and a time column into a single datetime64[ns] column.

    Assumes:
        - date_col contains datetime64, datetime.date, or string-parsable dates
        - time_col contains datetime.time objects

    Result:
        df[output_col] is a pandas datetime64[ns] column.
    """
    df = df.copy()

    # Ensure date column is pandas datetime
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    def _combine(d, t):
        if pd.isna(d) or t is None or not isinstance(t, dt.time):
            return pd.NaT
        return pd.Timestamp.combine(d.date(), t)

    df[output_col] = [_combine(d, t) for d, t in zip(df[date_col], df[time_col])]

    return df


def get_excel_sheets(excel_path: Path) -> dict[str, pd.DataFrame]:
    """Read all sheets from the given Excel file into a dictionary of
    DataFrames. Each DataFrame will have cleaned column names.
    """
    sheets = pd.read_excel(excel_path, sheet_name=None)
    for name, df in sheets.items():
        new_df = clean_column_names(df)
        sheets[name] = new_df
    return sheets


def flatten_data(sheets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    # Read the two sheets
    overview = sheets["Overview"]
    all_data = sheets["All Data"]
    # Flatten: attach overview metadata to every detection row
    flat = all_data.merge(
        overview,
        on="device",
        how="left",  # keep all detections even if some metadata missing
        validate="m:1",  # ensures only one overview row per device, no duplication of detections
    )
    # or more simply:
    overview_cols = overview.columns

    mask = flat[overview_cols].isna().all(axis=1)

    unmatched_devices = flat.loc[mask, "device"].unique()

    print("Devices missing overview metadata:", unmatched_devices)

    return flat
