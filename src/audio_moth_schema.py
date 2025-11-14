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
    date: pd.Timestamp = pa.Field(coerce=True)
    time: Series[pa.DateTime] = pa.Field(coerce=True, nullable=True)