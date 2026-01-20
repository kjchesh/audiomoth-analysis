""" "Tests to confirm the AudioMoth schema can take in the data and convert types as expected."""

import src.audio_moth_schema as audiomoth_schema
import pandas as pd
import pandas.api.types as ptypes


def test_validate_audiomoth_data(device_overview_df: pd.DataFrame) -> None:
    """Test that the Audiomoth data is validated correctly."""
    # ARRANGE
    df = device_overview_df.copy()
    # ACT
    validated_df = audiomoth_schema.AudioMothSchema.validate(df)

    # ASSERT
    # confirm that we are correctly using the schema to convert types
    assert not ptypes.is_datetime64_any_dtype(df["date"])
    assert ptypes.is_datetime64_any_dtype(validated_df["date"])
    assert not ptypes.is_datetime64_any_dtype(df["time"])
    assert ptypes.is_datetime64_any_dtype(validated_df["time"])
