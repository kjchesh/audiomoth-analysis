import pandas as pd
import pandera.pandas as pa
from pandera.typing.pandas import Series


class AudioMothSchema(pa.DataFrameModel):
    start_s: int = pa.Field(coerce=True)
    end_s: int = pa.Field(coerce=True)
    scientific_name: str = pa.Field(coerce=True)
    common_name: str = pa.Field(coerce=True)
    confidence: float = pa.Field(ge=0.0, le=1.0, coerce=True)
    file: str = pa.Field(coerce=True)
    date: Series[pd.Timestamp] = pa.Field(coerce=True)
    time: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)
    device: str = pa.Field(coerce=True)
    site: str = pa.Field(coerce=True)
    location_id: str = pa.Field(coerce=True)
    habitat: str = pa.Field(coerce=True)
    w3w: str = pa.Field(coerce=True)
    deployment_date: Series[pd.Timestamp] = pa.Field(coerce=True)
    deployment_time: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)
