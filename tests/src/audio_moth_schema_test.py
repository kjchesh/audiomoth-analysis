""" "Tests to confirm the AudioMoth schema can take in the data and convert types as expected."""

import pytest
import src.audio_moth_schema as audiomoth_schema
import pandas as pd
from pandera.errors import SchemaError


def test_validate_audiomoth_data(normalised_data_set: pd.DataFrame) -> None:
    """Test that the Audiomoth data is validated correctly."""
    # ARRANGE
    df = normalised_data_set.copy()
    # ACT
    validated_df = audiomoth_schema.AudioMothSchema.validate(df)

    # ASSERT
    # confirm that we are correctly using the schema to convert types
    assert pd.api.types.is_datetime64_any_dtype(validated_df["detection_timestamp"])
    assert pd.api.types.is_datetime64_any_dtype(validated_df["deployment_timestamp"])
    # Confirm only columns in schema are present
    assert set(validated_df.columns) == set(audiomoth_schema.AudioMothSchema.__fields__)  # type: ignore


def test_schema_drops_extra_columns(normalised_data_set: pd.DataFrame) -> None:
    df = normalised_data_set.copy()
    df["extra_column"] = "should be removed"

    validated_df = audiomoth_schema.AudioMothSchema.validate(df)

    assert "extra_column" not in validated_df.columns


def test_schema_fills_missing_columns(normalised_data_set: pd.DataFrame) -> None:
    df = normalised_data_set.copy()
    df = df.drop(columns=["habitat"])

    with pytest.raises(SchemaError):
        audiomoth_schema.AudioMothSchema.validate(df)
