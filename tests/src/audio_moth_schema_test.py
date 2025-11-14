""""Tests to confirm the AudioMoth schema can take in the data and convert types as expected."""
import src.audio_moth_schema as audiomoth_schema
import src.normaliser as normaliser
from io import StringIO
import pandas as pd
import pandas.api.types as ptypes

def test_validate_audiomoth_data() -> None:
    """ Test that the Audiomoth data is validated correctly. """
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

    df = normaliser.clean_audiomoth_column_names(df)
    # ACT
    validated_df = audiomoth_schema.AudioMothSchema.validate(df)

    # ASSERT
    # confirm that we are correctly using the schema to convert types
    assert not ptypes.is_datetime64_any_dtype(df["date"])
    assert ptypes.is_datetime64_any_dtype(validated_df["date"])
    assert not ptypes.is_datetime64_any_dtype(df["time"])
    assert ptypes.is_datetime64_any_dtype(validated_df["time"])