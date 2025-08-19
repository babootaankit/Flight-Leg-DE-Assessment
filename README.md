# Flight Status Deduplication

## Overview
This project deduplicates flight leg data and returns the most recent flight status record from the data provided.

## Latest Flight Function
This file provides the get_latest_flight function which takes in a filepath for flight leg data.

I've also included a commented out version of the function which also takes in id_col, date_col, and skiprows along with the filepath as parameters.

This makes the function much more adaptable to a table that may contain different column names and can be used to dedup any table based on the id and date columns.

I have previously deduped TechOps HR evaluation data by using groupby on the primary keys and idxmax with the date column. 
For example:
```python
    latest_flight_df = df.groupby(id_col)[date_col].idxmax()
    latest_flight_df = df.loc[latest_flight_df]
```
....but this took to long to run since the dataset was large. 

The logic in the function now uses sort_values + drop_duplicates then groups flights by flightkey and orders records so the most recent update appears first within each group. Then drop_dupliactes has the keep='first' parameter which drops duplicate rows but keeps the first record (latest date)

## Latest Flight Query
The query located in sql/latest_flight_query.sql uses JOIN and MAX(lastupdt) to retrieve the latest date for each record.

Another way of doing this can be to write a window function using ROW_NUMBER() and PARTITION BY flightkey to rank each row by flighkey and get the latest flight when you order by lastupdt and filter to rank=1

I think that writing a window function may be more useful for more complex data where more columnsa are involved but since this is a simple query I used the max date to get the latest lastupdt.

## How to Run
```bash
pip install -r requirements.txt
python main.py data/Data Engineer_Assessment_Data Set_Flight Leg.xlsx
