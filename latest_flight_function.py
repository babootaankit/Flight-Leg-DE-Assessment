# %%
import pandas as pd


def get_latest_flight(filepath: str) -> pd.DataFrame:
    """
    keeps latest date record in dataframe from the data ingested for each unique flight record

    Args:
        filepath (str): filepath of excel file containing data

    Returns:
        latest_flight_df (pd.DataFrame): transformed dataframe containing latest record for each flight
    """

    # create list of columns to read
    cols = [
        "flightkey",
        "flightnum",
        "flight_dt",
        "orig_arpt",
        "dest_arpt",
        "flightstatus",
        "lastupdt",
    ]

    # read in excel file and set to dataframe
    # header is set to 7 as the dataframe header starts off on the 8th row
    df = pd.read_excel(
        filepath,
        sheet_name="Dummy_Flight_Leg_Data",
        header=7,
        usecols=cols,
        engine="openpyxl",
    )

    # creat datetime with lastupdt and flight dt
    # Use errors='coerce' to drop bad dates
    df["lastupdt"] = pd.to_datetime(
        df["flight_dt"].astype(str) + " " + df["lastupdt"].astype(str), errors="coerce"
    )

    df = df.dropna(subset=["lastupdt", "flightkey"])

    # sort and drop duplicate values
    df = df.sort_values(["flightkey", "lastupdt"])
    latest_flight_df = df.drop_duplicates(subset="flightkey", keep="last").reset_index(
        drop=True
    )

    # order columns and drop ones not needed
    latest_flight_df = latest_flight_df[
        [
            "flightkey",
            "flightnum",
            "flight_dt",
            "orig_arpt",
            "dest_arpt",
            "flightstatus",
            "lastupdt",
        ]
    ]

    return latest_flight_df


# %%
# fp = "data\Data Engineer_Assessment_Data Set_Flight Leg.xlsx"

# df = get_latest_flight(fp)


# %%
# # function with more parameters
# import pandas as pd
# from pandas.api.types import is_datetime64_any_dtype

# def get_latest_flight(filepath: str, cols: list, header: int, id_col: str, date_col: str, sheet_name: str, ts_col: str=None) -> pd.DataFrame:
#     """
#     keeps latest date record in datafrmae from the data ingested for each unique flight record

#     Args:
#         filepath (str): filepath of excel file containing data

#         cols (list):
#             List of column names to load from the Excel file.

#         header (int):
#             Row number in the Excel file to use as the header.

#         id_col (str):
#             Column name that uniquely identifies each flight

#         date_col (str):
#             Primary date column used to sort

#         sheet_name (str):
#             Name of the sheet in the Excel file that contains the data.

#         ts_col (str, optional):
#             Column name containing timestamp or last updated time.
#             If provided, and if values are not already datetime, they will be
#             combined with `date_col` to create full datetime values.
#             Defaults to None.

#     Returns:
#         latest_flight_df (pd.DataFrame): transformed dataframe containing latest record for each flight
#     """

#     # create list of columns to read

#     df = pd.read_excel(filepath, sheet_name=sheet_name, header=header, usecols=cols, engine='openpyxl')

#     # creat datetime with lastupdt and flight dt
#     # Use errors='coerce' to drop bad dates
#     if is_datetime64_any_dtype(df[date_col]):
#         df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

#     else:
#         df[date_col] = pd.to_datetime(df[ts_col].astype(str) + ' ' + df[date_col].astype(str), errors='coerce')

#     df = df.dropna(subset=[date_col, id_col])

#     # sort and drop duplicate values
#     df = df.sort_values([id_col, date_col])
#     latest_flight_df = df.drop_duplicates(subset=id_col, keep='last').reset_index(drop=True)

#     # order columns and drop ones not needed
#     latest_flight_df = latest_flight_df[cols]

#     return latest_flight_df


if __name__ == "__main__":
    fp = "data\Data Engineer_Assessment_Data Set_Flight Leg.xlsx"

    df = get_latest_flight(fp)

    print(df)

    # fp = "data\Data Engineer_Assessment_Data Set_Flight Leg.xlsx"

    # cols = ['flightkey', 'flightnum', 'flight_dt', 'orig_arpt', 'dest_arpt', 'flightstatus', 'lastupdt']

    # df = get_latest_flight(filepath=fp, header=7, id_col='flightkey', date_col='lastupdt', cols=cols, sheet_name='Dummy_Flight_Leg_Data', ts_col='flight_dt')
