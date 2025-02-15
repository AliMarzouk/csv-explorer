from __future__ import annotations
from enum import Enum
from lib.core.utils import check_columns_in_df, check_columns_types
from lib.utils.constants import ColumnDataType
from lib.utils.utils import read_csv_into_df
import pandas as pd


class MissingValueReplaceOption(Enum):
    MEDIAN = "median"
    MEAN = "mean"
    PANDAS_LINEAR_INTERPOLATE = "linear_interpolate"
    CUSTOM_STRING_VALUE = "custom_string_internal_use_only"
    
    def get(value: str, default: any) -> MissingValueReplaceOption:
        from contextlib import suppress
        with suppress(KeyError): 
            return MissingValueReplaceOption[value]
        return default

def remove_missing_values(file_path: str, delimiter: str, cols_to_consider: list[str]=None, axis='index') -> pd.DataFrame:
    df = read_csv_into_df(file_path, delimiter)
    check_columns_in_df(df, cols_to_consider)
    df_dropped = df.dropna(axis=axis, subset=cols_to_consider)
    return df_dropped

def replace_missing_values(file_path: str, delimiter: str, column_names=[], value : MissingValueReplaceOption | str = None) -> pd.DataFrame:
    df = read_csv_into_df(file_path, delimiter)
    check_columns_in_df(df, column_names)
    for col_name in column_names:
        if value == MissingValueReplaceOption.MEAN:
            check_columns_types(df, column_names, [ColumnDataType.FLOATING, ColumnDataType.INTEGER])
            df[col_name] = df[col_name].fillna(df[col_name].mean())
        elif value == MissingValueReplaceOption.MEDIAN:
            check_columns_types(df, column_names, [ColumnDataType.FLOATING, ColumnDataType.INTEGER])
            df[col_name] = df[col_name].fillna(df[col_name].median())
        elif value == MissingValueReplaceOption.PANDAS_LINEAR_INTERPOLATE:
            check_columns_types(df, column_names, [ColumnDataType.FLOATING, ColumnDataType.INTEGER])
            df[col_name] = df[col_name].fillna(df[col_name].interpolate())
        else:
            df[col_name] = df[col_name].fillna(value)
    
    return df
    
def drop_columns(file_path: str, delimiter: str, column_names=[]) -> pd.DataFrame:
    df = read_csv_into_df(file_path, delimiter)
    check_columns_in_df(df, column_names)
    df_dropped = df.drop(labels=column_names, axis=1)
    return df_dropped
