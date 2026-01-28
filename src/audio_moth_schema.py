import pandera.pandas as pa
import pandas as pd
from pandera.typing import Series


class AudioMothSchema(pa.DataFrameModel):
    start_s: int = pa.Field()
    end_s: int = pa.Field()
    scientific_name: str = pa.Field()
    common_name: str = pa.Field()
    confidence: float = pa.Field(ge=0.0, le=1.0)
    detection_timestamp: Series[pd.Timestamp] = pa.Field(nullable=True)
    device: str = pa.Field()
    site: str = pa.Field()
    location_id: str = pa.Field()
    habitat: str = pa.Field()
    w3w: str = pa.Field()
    deployment_timestamp: Series[pd.Timestamp] = pa.Field(nullable=True)

    class Config:  # type: ignore
        coerce = True
        strict = "filter"
