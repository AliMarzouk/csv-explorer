import re
import pandas as pd

from lib.utils.constants import ColumnDataType


class ProcessingError(Exception):
    pass

class UtilsError(ProcessingError):
    pass

def check_columns_in_df(df: pd.DataFrame, column_names: list[str]) -> None:
    """Raises an exception if one the given column names is not found in the pandas dataframe.

    Args:
        df (pd.DataFrame): pandas data frame to check.
        column_names (list[str]): list of column names to check.

    Raises:
        AnanlysisError: exception raised if the column name is not found in the data frame.
    """
    for column_name in column_names:
        if column_name not in df.columns:
            raise UtilsError(f"Given column=[{column_name}] not found. Please choose one of the following {df.columns.tolist()}")
        
def determine_types(df: pd.DataFrame) -> dict[str, ColumnDataType]:
    """Returns a dictionnary of column data types by column names given a pandas data frame.

    Args:
        df (pd.DataFrame): data frame to determine column data types.

    Returns:
        dict[str, ColumnDataType]: column data types by column names.
    """
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

def check_columns_types(df: pd.DataFrame, column_names: list[str], allowed_types: list[ColumnDataType]) -> None:
    """Raises UtilsError exception if the given columns have a type that is not in the allowed types.

    Args:
        df (pd.DataFrame): data frame to check column types into.
        column_names (list[str]): column names to check.
        allowed_types (list[ColumnDataType]): allowed types to use in the check

    Raises:
        UtilsError: raised if one of the columns have a type that is not in the allowed types.
    """
    type_by_column = determine_types(df)
    columns_types: list[ColumnDataType] = [type_by_column[col_name] for col_name in column_names]
    for column_type in columns_types:
        if column_type not in allowed_types:
            raise UtilsError(f"Data has a column of type [{column_type.name}] wich is not allowed. Only {[a.name for a in allowed_types]} types are allowed")

