from lib.core.manipulation import MissingValueReplaceOption, remove_missing_values, replace_missing_values, drop_columns
from config.config import OUTPUT_CSV_FILE
from lib.utils.utils import write_df_into_csv


# axis can be either 'columns' / 1 or 'index' 0
def handle_missing_values(column_names: list[str] = [], replace_by: str=None, axis=0) -> None:
    replace_by = MissingValueReplaceOption.get(replace_by, replace_by)
    if not replace_by:
        df = remove_missing_values(OUTPUT_CSV_FILE, ',', column_names, axis)
    else:
        df = replace_missing_values(OUTPUT_CSV_FILE, ',', column_names, replace_by)
    write_df_into_csv(df, OUTPUT_CSV_FILE)
        
def remove_columns(column_names: list[str] = []) -> None:
    df = drop_columns(OUTPUT_CSV_FILE, ',', column_names)
    write_df_into_csv(df, OUTPUT_CSV_FILE)
