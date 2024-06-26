import os
from typing import Union
import pandas as pd

ROOT_PATH = os.getcwd().replace('\\', '/')
SAVE_PATH = ROOT_PATH + '/scripts/dataset/'


def save_to_csv(results: Union[list, pd.DataFrame], filename: str):
    try:
        if isinstance(results, list):
            if len(results) == 0:
                return
            df = pd.DataFrame(results)
        elif isinstance(results, pd.DataFrame):
            df = results
        else:
            raise TypeError("O argumento 'results' deve ser uma lista ou DataFrame do pandas.")

        df.to_csv(SAVE_PATH + filename, index=False)
        print(f"Resultados salvos em '{filename}'")

    except Exception as e:
        print(f"Erro ao salvar em CSV: {e}")


def read_csv(filename: str, type='list' or 'dataframe', columns: list = None):
    try:
        df = pd.read_csv(SAVE_PATH + filename)
        print(df.head())
        print()

        if type == 'list':
            df = df[columns] if columns else df
            results = df.to_dict('records')
            if len(results) > 0:
                return results
        
        elif type == 'dataframe':
            return df
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado")

def merge_data(repo_df: list, pr_df: list, column_join: str):
    try:
        repo_df = pd.DataFrame(repo_df)
        pr_df = pd.DataFrame(pr_df)

        combined_data = pd.merge(repo_df, pr_df, on=column_join, how='inner').fillna(0)
        return combined_data
    except Exception as e:
        print(f"Erro: Não foi possível fazer o merge {e}")
