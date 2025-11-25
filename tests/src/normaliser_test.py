"""Tests to check normalisation of column names in Normaliser.py"""

import src.normaliser as normaliser
import pandas as pd
from pathlib import Path
import datetime as dt


MOCK_OVERVIEW_DF = pd.DataFrame(
    {
        "device": ["AM123", "AM124"],
        "site": ["SiteA", "SiteB"],
        "location_id": ["SA1", "SB1"],
        "habitat": ["Forest", "Grassland"],
        "W3W": ["mock.three.words", "three.mocked.words"],
        "deployment_date": ["2025-02-10", "2025-02-11"],
        "deployment_time": ["12:00:00", "13:00:00"],
    }
)

MOCK_DEVICE_DF = pd.DataFrame(
    {
        "start_s": [27, 25],
        "end_s": [30, 33],
        "scientific_name": ["Strix aluco", "Troglodytes troglodytes"],
        "common_name": ["Tawny Owl", "Eurasian Wren"],
        "confidence": [0.8164, 0.9123],
        "file": [
            "D:/Feb 10 - 16\\20250210_130500.WAV",
            "D:/Feb 10 - 16\\20250211_131000.WAV",
        ],
        "date": ["10-02-2025", "10-02-2025"],
        "time": ["13:05:00", "13:10:00"],
    }
)

MOCK_MERGED_DEVICE_DF = pd.DataFrame(
    {
        "start_s": [27, 25, 27, 25],
        "end_s": [30, 33, 30, 33],
        "scientific_name": [
            "Strix aluco",
            "Troglodytes troglodytes",
            "Strix aluco",
            "Troglodytes troglodytes",
        ],
        "common_name": ["Tawny Owl", "Eurasian Wren", "Tawny Owl", "Eurasian Wren"],
        "confidence": [0.8164, 0.9123, 0.8164, 0.9123],
        "file": [
            "D:/Feb 10 - 16\\20250210_130500.WAV",
            "D:/Feb 10 - 16\\20250211_131000.WAV",
            "D:/Feb 10 - 16\\20250210_130500.WAV",
            "D:/Feb 10 - 16\\20250211_131000.WAV",
        ],
        "date": ["10-02-2025", "10-02-2025", "10-02-2025", "10-02-2025"],
        "time": ["13:05:00", "13:10:00", "13:05:00", "13:10:00"],
        "device": ["AM123", "AM123", "AM124", "AM124"],
        "site": ["SiteA", "SiteA", "SiteB", "SiteB"],
        "location_id": ["SA1", "SA1", "SB1", "SB1"],
        "habitat": ["Forest", "Forest", "Grassland", "Grassland"],
        "W3W": [
            "mock.three.words",
            "mock.three.words",
            "three.mocked.words",
            "three.mocked.words",
        ],
        "deployment_date": ["2025-02-10", "2025-02-10", "2025-02-11", "2025-02-11"],
        "deployment_time": ["12:00:00", "12:00:00", "13:00:00", "13:00:00"],
    }
)


def test_clean_audiomoth_data():
    """Test that the Audiomoth data is cleaned correctly."""
    # ARRANGE
    df = pd.DataFrame(
        {
            "Start (s)": [27, 25],
            "End (s)": [30, 33],
            "Scientific Name": ["Strix aluco", "Troglodytes troglodytes"],
            "Common Name": ["Tawny Owl", "Eurasian Wren"],
            "Confidence": [0.8164, 0.9123],
            "File": ["D:/Feb 10 - 16\\20250210_130500.WAV"] * 2,
            "Date": ["10-02-2025", "10-02-2025"],
            "Time": ["13:05:00", "13:10:00"],
        }
    )
    # ACT
    df = normaliser.clean_column_names(df)
    # ASSERT
    expected_columns = MOCK_DEVICE_DF.columns.tolist()
    assert list(df.columns) == expected_columns


def test_combine_date_and_time():
    # ARRANGE
    df = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", None],
            "time": [
                dt.time(13, 5),
                dt.time(7, 30),
                dt.time(22, 45),  # but date is NaT → result should be NaT
            ],
        }
    )

    # Expected combined timestamp results
    expected = pd.Series(
        [
            pd.Timestamp("2024-01-01 13:05:00"),
            pd.Timestamp("2024-01-02 07:30:00"),
            pd.NaT,
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


def test_get_excel_sheets() -> None:
    """Test that we can read all sheets from an Excel file."""
    # ARRANGE
    excel_content = {
        "Overview": MOCK_OVERVIEW_DF,
        "AM123": MOCK_DEVICE_DF,
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


def test_flatten_data():
    """Test to confirm flattening of device data with overview metadata behaves
    as expected."""
    # ARRANGE
    device_df = MOCK_DEVICE_DF.copy()
    device_df_2 = MOCK_DEVICE_DF.copy()
    overview_df = MOCK_OVERVIEW_DF.copy()
    sheets = {
        "overview": overview_df,
        "AM123": device_df,
        "AM124": device_df_2,
    }
    # ACT
    merged_df = normaliser.flatten_data(sheets)
    # ASSERT
    # ensure the merged dataframe matches the expected dataframe
    pd.testing.assert_frame_equal(
        merged_df.reset_index(drop=True), MOCK_MERGED_DEVICE_DF
    )
