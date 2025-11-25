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
    """Read all sheets from the given Excel file into a dictionary of DataFrames."""
    sheets = pd.read_excel(excel_path, sheet_name=None)
    for name, df in sheets.items():
        df = clean_column_names(df)
    return sheets


def flatten_data(sheets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Combine the Overview sheet with all device sheets and return a single
    flat DataFrame where each row represents one detection event.

    Assumes:
        - "Overview" contains device metadata (location, deployment dates, etc.)
        - Each remaining sheet is a device, and the sheet name is the device_id
    """
    # Split out the overview sheet, keep the rest as device sheets
    overview_df = sheets.pop("overview")  # overview_df is now your metadata
    # table
    device_dfs = []

    for sheet_name, df in sheets.items():
        device_id = sheet_name  # sheet name == device id

        # Find the matching row in the overview sheet
        meta_row = overview_df.loc[overview_df["device"] == device_id]

        if meta_row.empty:
            # No metadata found for this device – you can skip or warn
            print(f"Warning: no overview metadata for device '{device_id}'")
            continue

        # Take the first (and usually only) matching row as a Series
        meta = meta_row.iloc[0]

        # Optionally add device_id as a column to the device dataframe
        if "device" not in df.columns:
            df["device"] = device_id

        # Broadcast all metadata columns onto each row of this device df
        for col, val in meta.items():
            # Avoid overwriting existing columns in the device data
            if col not in df.columns:
                df[col] = val

        device_dfs.append(df)

    # Combine all device dataframes into one big dataframe
    combined_df = pd.concat(device_dfs, ignore_index=True)

    return combined_df
