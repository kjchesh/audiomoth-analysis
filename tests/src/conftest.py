import pandas as pd
import pytest


@pytest.fixture
def overview_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "device": ["AM123", "AM124"],
            "site": ["SiteA", "SiteB"],
            "location_id": ["SA1", "SB1"],
            "habitat": ["Forest", "Grassland"],
            "w3w": ["mock.three.words", "three.mocked.words"],
            "deployment_date": ["2025-02-10", "2025-02-11"],
            "deployment_time": ["12:00:00", "13:00:00"],
        }
    )


@pytest.fixture
def device_df() -> pd.DataFrame:
    return pd.DataFrame(
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


@pytest.fixture
def device_overview_df() -> pd.DataFrame:
    return pd.DataFrame(
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
            "w3w": [
                "mock.three.words",
                "mock.three.words",
                "three.mocked.words",
                "three.mocked.words",
            ],
            "deployment_date": ["2025-02-10", "2025-02-10", "2025-02-11", "2025-02-11"],
            "deployment_time": ["12:00:00", "12:00:00", "13:00:00", "13:00:00"],
        }
    )
