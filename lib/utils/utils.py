
import pandas as pd

def read_csv_into_df(file_path: str, delimiter: str) -> pd.DataFrame:
    # TODO: add raising / handling exception
    return pd.read_csv(file_path, sep=delimiter)