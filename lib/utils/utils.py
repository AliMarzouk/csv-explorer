
import pandas as pd

def read_csv_into_df(file_path: str, delimiter: str) -> pd.DataFrame:
    # TODO: add raising / handling exception
    df = pd.read_csv(file_path, sep=delimiter)
    # df.drop('Unnamed: 0', axis=1, inplace=True)
    return df

def write_df_into_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)