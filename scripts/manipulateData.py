from pandas import DataFrame
import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv
from queries import repo_query, pr_query
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = 'https://api.github.com/graphql'
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}


def run_query(query, variables=None):
    time.sleep(0.01)
    
    response = requests.post(
        API_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    if response.status_code == 200:
        return response.json(), response.status_code
    
    print(f"Erro na consulta GraphQL ({response.status_code})")
    time.sleep(1)
    
    return False, response.status_code


def get_repo_data(num_repos: int, per_page: int, repo_results: list=[]) -> list:
    print(f"Buscando {num_repos} repositórios...")
    start_time = time.time()

    initial_repo_results_len = len(repo_results)
    has_next_page: bool = True
    cursor: str = repo_results[-1] if initial_repo_results_len > 0 else None
    req_errors = 0

    try:
        while len(repo_results) < num_repos and has_next_page:
            variables = {
                "perPage": per_page,
                "cursor": cursor
            }

            data, status_code = run_query(query=repo_query, variables=variables)
            
            if not data:
                req_errors += 1
                
                continue
            
            if 'errors' in data:
                print(f"Erro na consulta GraphQL({status_code}): { data['errors'][0]['message'] }")
                req_errors += 1
                
                continue
                
            cursor = data["data"]["search"]["pageInfo"]["endCursor"]

            for edges in data["data"]["search"]["edges"]:
                repo_info = edges["node"]
                repo_name_with_owner = repo_info["nameWithOwner"]
                stargazers_count = repo_info["stargazers"]["totalCount"]
                pr_count = repo_info["pullRequests"]["totalCount"]
                   
                result_info = {
                    "Repositório": repo_name_with_owner,
                    "Estrelas": stargazers_count,
                    "Pull Requests": pr_count
                }
                
                repo_results.append(result_info)
                    

            has_next_page = data["data"]["search"]["pageInfo"]["hasNextPage"]
            if not has_next_page:
                break

    except Exception as e:
        print(f"\nErro durante a execução da consulta: {e}")
        print("Salvando itens encontrados até agora em arquivo CSV...\n")
    
    finally:
        end_time = time.time()
        print(f"{len(repo_results) - initial_repo_results_len} repositórios encontrados")
        print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
        print(f"Total de erros: {req_errors} ({req_errors / num_repos * 100:.2f}%)")

        return repo_results


def get_pr_data(repo_results: list=[], pr_results: list=[]) -> list:
    print("Buscando informações dos Pull Requests...")
    start_time = time.time()
    
    initial_pr_results_len = len(pr_results)
    cursor: str = pr_results[-1] if initial_pr_results_len > 0 else None
    req_errors = 0
       
    try:
        for repo in repo_results:
            if any(repo["Repositório"] == pr["Repositório"] for pr in pr_results):
                continue
            
            owner, repo_name = repo["Repositório"].split("/")
            pr_variables = {"owner": owner, "name": repo_name}
            data, status_code = run_query(query=pr_query, variables=pr_variables)
            
            if not data:
                print(f"Pulando repositório {repo["Repositório"]}...")
                req_errors += 1
                
                continue
            
            if 'errors' in data:
                print(f"Erro na consulta GraphQL({status_code}): { data['errors'][0]['message'] }")
                req_errors += 1
                
                continue
            
            for edge in data["data"]["repository"]["pullRequests"]["edges"]:
                node = edge["node"]

                review_quant = node["reviews"]["totalCount"]
                if review_quant < 1:
                    continue
                
                data_criacao_dt = datetime.fromisoformat(node["createdAt"].replace("Z", "+00:00"))
                data_fechamento_dt = datetime.fromisoformat(node["closedAt"].replace("Z", "+00:00"))
                corpo_pr = node["bodyText"].replace("\n", "")

                if node["mergedAt"]:
                    data_merge_dt = datetime.fromisoformat(node["mergedAt"].replace("Z", "+00:00"))
                    interval_dates = data_merge_dt - data_criacao_dt
                else:
                    data_merge_dt = None
                    interval_dates = data_fechamento_dt - data_criacao_dt

                info = {
                    "Repositório": repo["Repositório"],
                    "Estado PR": node["state"],
                    "Número PR": node["number"],
                    "Data de Criação PR": data_criacao_dt,
                    "Data de Fechamento PR": data_fechamento_dt,
                    "Data de Merge PR": data_merge_dt,
                    "Intervalo Criação e Última Atividade": round(interval_dates.total_seconds() / 3600, 2),
                    "Status Revisão": node["reviewDecision"],
                    "Revisões": review_quant,
                    "Arquivos Alterados": node["files"]["totalCount"],
                    "Linhas Adicionadas": node["additions"],
                    "Linhas Excluídas": node["deletions"],
                    "Caracteres Corpo PR": len(corpo_pr),
                    "Participantes PR": node["participants"]["totalCount"],
                    "Comentários PR": node["comments"]["totalCount"],
                    "Cursor": cursor
                }
                
                pr_results.append(info)
                    
    except Exception as e:
        print(f"\nErro durante a execução da consulta: {e}")
        print("Salvando itens encontrados até agora em arquivo CSV...\n")

    finally:
        end_time = time.time()
        final_pr_results_len = len(pr_results)
        print(f"\n{final_pr_results_len - initial_pr_results_len} Pull Requests encontrados")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
        print(f"Total de erros: {req_errors} ({req_errors / final_pr_results_len * 100:.2f}%)")
        
        return pr_results

def summarized_data(df: DataFrame, columns: list):
    import pandas as pd

    median_per_repo = df.groupby('Repositório')[columns].median(numeric_only=True).round(2).fillna(0)
    total_data_per_repo = df.groupby('Repositório')[["Revisões", "Comentários PR", "Participantes PR"]].sum().fillna(0)
    media_data_per_repo = df.groupby('Repositório')[["Arquivos Alterados", "Linhas Adicionadas", "Linhas Excluídas"]].mean().fillna(0)
    status_counts = df.groupby(['Repositório', 'Status Revisão']).size().unstack(fill_value=0)
    resultados = pd.concat(
        [median_per_repo, total_data_per_repo, media_data_per_repo, status_counts], axis=1)

    resultados.reset_index(inplace=True)

    return resultados


def get_correlation_coefficient(df: DataFrame, columns: list):
    from scipy.stats import spearmanr

    group1 = df[columns[0]]
    group2 = df[columns[1]]
    correlation_coefficient, p = spearmanr(group1, group2)

    return correlation_coefficient, p