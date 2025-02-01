from lib.core.analysis import count_values_by_columns, find_outliers_by_columns, get_missing_values_indexes_by_columns
from lib.utils.utils import read_csv_into_df
from config.config import OUTPUT_CSV_FILE 

def read_csv_file(local_path: str, delimiter: str):
    df = read_csv_into_df(local_path, delimiter)
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    
def count_missing_values(column_names: list[str] = [], additional_null_values: list[str] = []) -> dict[str, int]:
    missing_values_indexes_by_col = get_missing_values_indexes_by_columns(OUTPUT_CSV_FILE, ',', column_names, additional_null_values)
    return {key: len(value) for key, value in missing_values_indexes_by_col.items()}

def count_values(column_names: list[str] = []) -> dict[str, dict[str, int]]:
    return count_values_by_columns(OUTPUT_CSV_FILE, ',', column_names)

def find_outliers(column_names: list[str] = []) -> dict[str, list[str]]:
    return find_outliers_by_columns(OUTPUT_CSV_FILE, ',', column_names)