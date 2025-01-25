import pandas as pd
import re

from lib.utils.constants import ColumnDataType

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
    df = pd.read_csv(file_path, sep=delimiter)

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

# print(determine_types('amazon.csv', ','))