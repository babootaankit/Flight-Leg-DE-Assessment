# Flight Status Deduplication

## Overview
This project deduplicates flight leg data and returns the most recent flight status record from the data provided.

## How to Run
```bash
pip install -r requirements.txt
python latest_flight_function.py
```
Example:
```python
from latest_flight_function import get_latest_flight

# Path to the Excel file with flight leg data
filepath = "Data Engineer_Assessment_Data Set_Flight Leg.xlsx"

# Run the function
df = get_latest_flight(filepath)

# Display first five rows in df
print(df.head(5))
```

## Latest Flight Function
This file provides the get_latest_flight function which takes in a filepath for flight leg data.

I've also included a commented out version of the function which also takes in id_col, date_col, and skiprows along with the filepath as parameters.

This makes the function much more adaptable to a table that may contain different column names and can be used to dedup any table based on the id and date columns.

The goal of these functions is to return exactly one row per flight (flightkey) representing the most recent status update.

The primary key for deduping the data is flightkey which is treated as the unique flight identifier for grouping.

There is also a strategy being used to build a proper timestamp by combining flight_dt + lastupdt. Originally I only tried converting the lastupdt column to datetime but it did not work as it is not a proper timestamp and after using coerece, the resulting df had all NaT values in the lastupdt field.

I have previously deduped TechOps HR evaluation data by using groupby on the primary keys and idxmax with the date column in ztopoap_data.HR_EVAL_FACT. 

For example:
```python
    latest_flight_df = df.groupby(id_col)[date_col].idxmax()
    latest_flight_df = df.loc[latest_flight_df]
```
I did try this solution for this assignment, but this took to long to run since the dataset was large in this scenario. 

The logic in the function now uses sort_values + drop_duplicates then groups flights by flightkey and orders records so the most recent update appears first within each group. Then drop_dupliactes has the keep='first' parameter which drops duplicate rows but keeps the first record (latest date)

## Latest Flight Query
The query located in sql/latest_flight_query.sql uses JOIN and MAX(lastupdt) to retrieve the latest date for each record.

Another way of doing this can be to write a window function using ROW_NUMBER() and PARTITION BY flightkey to rank each row by flighkey and get the latest flight when you order by lastupdt and filter to rank=1

I think that writing a window function may be more useful for more complex data where more columnsa are involved but since this is a simple query I used the max date to get the latest lastupdt.

## Latest Flight Function Unit Testing
Run the unit test using pytest -v

pytest already looks in any folder called 'tests/' and for any file starting with 'test_'.py. -v shows each test name and its result.

On my current team in TechOps OAP, we rely on unittest.mock for unit testing, and we have started to leverage AI tools to accelerate writing these. The unit test included here reflect the style and practices I use in our production repositories (such as oautils and OAPETL). For this assessment, I also used AI assistance to quickly generate the test skeleton, then adapted it to align with our testing format.

## CI/CD
This repository includes a .gitlab-ci.yml file as an example of how I would organize a pipeline in a production setting. The structure is based on testing, lint, and deploy which is a simplified version of whay my team uses.

The test stage sets up the environment, installs the dependencies, and runs pytest. Linting runs tools like black and isort to keep the code style consistent. The deploy stage is left as a placeholder, but in a real environment it could handle things like publishing a package, generating docs, or pushing artifacts.
