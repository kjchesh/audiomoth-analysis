import pandera.pandas as pa
import pandas as pd
from pandera.typing import Series


class AudioMothSchema(pa.DataFrameModel):
    start_s: int = pa.Field(coerce=True)
    end_s: int = pa.Field(coerce=True)
    scientific_name: str = pa.Field(coerce=True)
    common_name: str = pa.Field(coerce=True)
    confidence: float = pa.Field(ge=0.0, le=1.0, coerce=True)
    detection_timestamp: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)
    device: str = pa.Field(coerce=True)
    site: str = pa.Field(coerce=True)
    location_id: str = pa.Field(coerce=True)
    habitat: str = pa.Field(coerce=True)
    w3w: str = pa.Field(coerce=True)
    deployment_timestamp: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)

    class Config:  # type: ignore
        coerce = True
        strict = "filter"  # extra columns not in schema
