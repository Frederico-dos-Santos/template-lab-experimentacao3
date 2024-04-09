import os
import pandas as pd

ROOT_PATH = os.getcwd().replace('\\', '/')
SAVE_PATH = ROOT_PATH + '/scripts/dataset/'

def save_to_csv(results : list, filename : str):
    try:
        df = pd.DataFrame(results)
        df.to_csv(SAVE_PATH + filename, index=False)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado")

def read_csv(filename : str):
    try:
        df = pd.read_csv(SAVE_PATH + filename)
        print(df.head())
        print()

        results = df.to_dict('records')
        if len(results) > 0:
            return results
        
        return None
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado")
        return None

def merge_data(repo_df : list, pr_df : list, column_join):
    repo_df = pd.DataFrame(repo_df)
    pr_df = pd.DataFrame(pr_df)
    
    combined_data = pd.merge(repo_df, pr_df, on=column_join, how='inner')
    return combined_data