"""Tests to check normalisation of column names in Normaliser.py"""

import src.normaliser as normaliser
import pandas as pd
from pathlib import Path
import datetime as dt


def test_clean_audiomoth_data(device_df: pd.DataFrame):
    """Test that the Audiomoth data is cleaned correctly."""
    # ARRANGE
    df = pd.DataFrame(
        {
            "Start (s)": [27, 25],
            "End (s)": [30, 33],
            "Scientific Name": ["Strix aluco", "Troglodytes troglodytes"],
            "Common Name": ["Tawny Owl", "Eurasian Wren"],
            "Confidence": [0.8164, 0.9123],
            "Date": ["10-02-2025", "10-02-2025"],
            "Time": ["13:05:00", "13:10:00"],
        }
    )
    # ACT
    df = normaliser.clean_column_names(df)
    # ASSERT
    expected_columns = device_df.columns.tolist()
    assert list(df.columns) == expected_columns


def test_combine_date_and_time():
    # ARRANGE
    df = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", None, "2024-01-04"],
            "time": [
                dt.time(13, 5),
                dt.time(7, 30),
                dt.time(22, 45),  # but date is NaT → result should be NaT
                "12:34",
            ],
        }
    )

    # Expected combined timestamp results
    expected = pd.Series(
        [
            pd.Timestamp("2024-01-01 13:05:00"),
            pd.Timestamp("2024-01-02 07:30:00"),
            pd.NaT,
            pd.Timestamp("2024-01-04 12:34:00"),
        ],
        name="timestamp",
        dtype="datetime64[ns]",
    )

    # ACT
    result = normaliser.combine_date_and_time(
        df, "date", "time", output_col="timestamp"
    )

    # ASSERT
    assert "timestamp" in result.columns
    assert result["timestamp"].dtype == "datetime64[ns]"

    # Compare the output column to expected
    pd.testing.assert_series_equal(result["timestamp"], expected)


def test_get_excel_sheets(overview_df: pd.DataFrame, device_df: pd.DataFrame) -> None:
    """Test that we can read all sheets from an Excel file."""
    # ARRANGE
    excel_content = {
        "overview": overview_df,
        "AM123": device_df,
    }
    excel_path = "mock_audiomoth.xlsx"
    with pd.ExcelWriter(excel_path) as writer:
        for sheet_name, df in excel_content.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    # ACT
    sheets = normaliser.get_excel_sheets(Path(excel_path))
    # ASSERT
    assert set(sheets.keys()) == set(excel_content.keys())
    for sheet_name, df in sheets.items():
        pd.testing.assert_frame_equal(
            df.reset_index(drop=True), excel_content[sheet_name]
        )


def test_flatten_data(
    overview_df: pd.DataFrame,
    all_devices_df: pd.DataFrame,
    flattened_data_set: pd.DataFrame,
) -> None:
    """Test to confirm flattening of device data with overview metadata behaves
    as expected."""
    # ARRANGE
    devices_df = all_devices_df.copy()
    overview_df = overview_df.copy()
    sheets = {
        "Overview": overview_df,
        "All Data": devices_df,
    }
    # ACT
    merged_df = normaliser.flatten_data(sheets)
    # ASSERT
    # ensure the merged dataframe matches the expected dataframe
    pd.testing.assert_frame_equal(merged_df.reset_index(drop=True), flattened_data_set)
