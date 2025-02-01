from lib.core.analysis import count_rows, count_values_by_columns, determine_types, find_outliers_by_columns, get_missing_values_indexes_by_columns
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

def get_header_infos() -> dict[str, list[str]]:
    data_type_by_col = determine_types(OUTPUT_CSV_FILE, ',')
    missing_values_indexes_by_col = get_missing_values_indexes_by_columns(OUTPUT_CSV_FILE, ',', [], [])
    rows_count = count_rows(OUTPUT_CSV_FILE, ',')
    result = {col_name: [data_type.value] for col_name, data_type in data_type_by_col.items()}
    result = {col_name: [*result[col_name], len(missing_indexes)] for col_name, missing_indexes in missing_values_indexes_by_col.items()}
    return {col_name: [*result_infos, rows_count] for col_name, result_infos in result.items()}