# %%
import pandas as pd
import os
import sys
from unittest import mock

import_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
sys.path.insert(0, import_path)
import latest_flight_function

def test_get_latest_flight_dedup():
    # Dummy input simulating an Excel read
    dummy_df = pd.DataFrame({
        "flightkey": ["DL123", "DL123", "DL124"],
        "flightnum": [3401, 3401, 31],
        "flight_dt": ["2019-01-01", "2019-01-01", "2019-01-01"],
        "orig_arpt": ["ATL", "ATL", "ATL"],
        "dest_arpt": ["LAX", "LAX", "DFW"],
        "flightstatus": ["Boarding", "In", "Boarding"],
        "lastupdt": ["09:02:17", "09:20:17", "09:17:00"]
    })

    # Patch pd.read_excel to return dummy_df instead of reading a file
    with mock.patch("pandas.read_excel", return_value=dummy_df):
        result = latest_flight_function.get_latest_flight("fake_path.xlsx")

    # 1) Should only return one row per flightkey
    assert result["flightkey"].nunique() == len(result)

    # 2) DL123 should keep the later status "In"
    dl123_row = result[result["flightkey"] == "DL123"].iloc[0]
    assert dl123_row["flightstatus"] == "In"

    # 3) lastupdt should be parsed to datetime
    assert pd.api.types.is_datetime64_any_dtype(result["lastupdt"])