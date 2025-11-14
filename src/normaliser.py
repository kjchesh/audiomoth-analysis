""" The audiomoth data needs some basic cleaning to have consistent column names and types."""

import pandas as pd

def clean_audiomoth_column_names(audiomoth_df: pd.DataFrame) -> pd.DataFrame:
    """ Clean the Audiomoth dataframe to have consistent column names and types. """
    # Lowercase/underscore column names
    audiomoth_df = audiomoth_df.rename(columns={c: c.strip().lower().replace(' ', '_').replace('(', '').replace(')', '') for c in audiomoth_df.columns})
    return audiomoth_df

