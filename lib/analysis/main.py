import pandas as pd
import numpy as np
import re

from lib.utils.constants import ColumnDataType
from lib.utils.utils import read_csv_into_df

class AnanlysisException(Exception):
    pass

def determine_types(file_path: str, delimiter: str) -> dict[str, ColumnDataType]:
    """Guesses the types of the given CSV file columns.
    
    Uses the pandas package to infer the data type of the CSV columns.
    The possible data type values are defined in the enum ColumnDataType. 

    Args:
        file_path (str): local path of the file.
        delimiter (str): delimiter of the file. Ex. ',' in CSV files.

    Returns:
        dict[str, ColumnTColumnDataTypeype]: mapping of the column name and the data type.
    """
    # Read the CSV file using the specified delimiter and header settings
    df = read_csv_into_df(file_path, delimiter)

    # Initialize a dictionary to store column data types
    column_types = {}

    # Loop through columns and infer data types
    for column in df.columns:
        # Check for datetime format "YYYY-MM-DD HH:MM:SS"
        is_datetime = all(re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str(value)) for value in df[column])

        # Check for date format "YYYY-MM-DD"
        is_date = all(re.match(r'\d{4}-\d{2}-\d{2}', str(value)) for value in df[column])

        # Assign data type based on format detection
        if is_datetime:
            inferred_type = ColumnDataType.DATETIME
        elif is_date:
            inferred_type = ColumnDataType.DATE
        else:
            inferred_type = ColumnDataType(pd.api.types.infer_dtype(df[column], skipna=True))

        column_types[column] = inferred_type

    return column_types

def get_missing_values_indexes(file_path: str, delimiter: str, column_name: str, additional_null_values: list[str] = []) -> list[int]:
    """Returns a list of indexes of values considered as null (nullish) in the CSV columns.
    
    Args:
        file_path (str): local path to the csv file.
        delimiter (str): delimiter character of the data.
        column_name (str): name of the column where to look for null values
        additional_null_values (list[str], optional): string values to consider as null. Defaults to [].

    Raises:
        AnanlysisException: raised if the given column name does not exist in the csv file.

    Returns:
        list[int]: indexes of the nullish values
    """
    df = read_csv_into_df(file_path, delimiter)
    
    if column_name not in df.columns:
        raise AnanlysisException(f"Given column=[{column_name}] not found in csv file path=[{file_path}]")
    
    missing_vlaues_condition = df[column_name].isnull() | df[column_name].isin(additional_null_values)
    return np.where(missing_vlaues_condition)[0].tolist()