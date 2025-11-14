""" Tests to check normalisation of column names in Normaliser.py """
import src.normaliser as normaliser
from io import StringIO
import pandas as pd
import pandas.api.types as ptypes

def test_clean_audiomoth_data():
    """ Test that the Audiomoth data is cleaned correctly. """
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
    df = normaliser.clean_audiomoth_column_names(df)
    # ASSERT
    expected_columns = [
        "start_s",
        "end_s",
        "scientific_name",
        "common_name",
        "confidence",
        "file",
        "date",
        "time",
    ]
    assert list(df.columns) == expected_columns


