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
    response = requests.post(
        API_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    
    print(f"Erro na consulta GraphQL: {response.status_code}")
    time.sleep(5)
    
    return False


def get_repo_data(num_repos: int, per_page: int, results: list=[]) -> list:
    print(f"Buscando {num_repos} repositórios...")
    start_time = time.time()

    cursor: str = None
    has_next_page: bool = True
    current_results_len = len(results)
    req_errors = 0

    try:
        while len(results) < num_repos and has_next_page:
            variables = {
                "perPage": per_page,
                "cursor": cursor
            }

            data = run_query(query=repo_query, variables=variables)
            if not data:
                req_errors += 1
                continue
            
            if 'errors' in data:
                raise Exception(
                    f"Erro na consulta GraphQL: { data['errors'][0]['message'] }")
                
                
            cursor = data["data"]["search"]["pageInfo"]["endCursor"]

            for edges in data["data"]["search"]["edges"]:
                repo_info = edges["node"]
                repo_name_with_owner = repo_info["nameWithOwner"]
                stargazers_count = repo_info["stargazers"]["totalCount"]

                pr_count = repo_info["pullRequests"]["totalCount"]

                result_info = {
                    "Repositório": repo_name_with_owner,
                    "Estrelas": stargazers_count,
                    "Pull Requests": pr_count,
                }
                results.append(result_info)

            has_next_page = data["data"]["search"]["pageInfo"]["hasNextPage"]
            if not has_next_page:
                break

    except Exception as e:
        print(f"\nErro durante a execução da consulta: {e}")
        print("Salvando itens encontrados até agora em arquivo CSV...\n")
    
    finally:
        end_time = time.time()
        print(f"{len(results) - current_results_len} repositórios encontrados")
        print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
        print(f"Total de erros: {req_errors} ({req_errors / num_repos * 100:.2f}%)")

        return results


def get_pr_data(repos: list, results: list=[]) -> list:
    print("Buscando informações dos Pull Requests...")
    start_time = time.time()
    
    req_errors = 0
    current_results_len = len(results)
        
    try:
        for repo in repos:
            existe = any(repo["Repositório"] == result["Repositório"]
                         for result in results)
            if existe:
                continue

            owner, repo_name = repo["Repositório"].split("/")
            pr_variables = {"owner": owner, "name": repo_name}
            data = run_query(query=pr_query, variables=pr_variables)

            if not data:
                req_errors += 1
                continue

            prs = []
            for edge in data["data"]["repository"]["pullRequests"]["edges"]:
                node = edge["node"]

                data_criacao_dt = datetime.fromisoformat(
                    node["createdAt"].replace("Z", "+00:00"))
                data_fechamento_dt = datetime.fromisoformat(
                    node["closedAt"].replace("Z", "+00:00"))
                corpo_pr = node["bodyText"].replace("\n", "\\n")

                if node["mergedAt"]:
                    data_merge_dt = datetime.fromisoformat(
                        node["mergedAt"].replace("Z", "+00:00"))
                    interval_dates = max(
                        data_merge_dt, data_fechamento_dt) - data_criacao_dt
                else:
                    data_merge_dt = None
                    interval_dates = data_fechamento_dt - data_criacao_dt

                info = {
                    "Repositório": repo["Repositório"],
                    "Estado PR": node["state"],
                    "Título PR": node["title"],
                    "Número PR": node["number"],
                    "Data de Criação PR": data_criacao_dt,
                    "Data de Fechamento PR": data_fechamento_dt,
                    "Data de Merge PR": data_merge_dt,
                    "Intervalo Criação e Última Atividade": round(interval_dates.total_seconds() / 3600, 2),
                    "Status Revisão": node["reviewDecision"],
                    "Revisões": node["reviews"]["totalCount"],
                    "Arquivos Alterados": node["files"]["totalCount"],
                    "Linhas Adicionadas": node["additions"],
                    "Linhas Excluídas": node["deletions"],
                    "Caracteres Corpo PR": len(corpo_pr),
                    "Participantes PR": node["participants"]["totalCount"],
                    "Comentários PR": node["comments"]["totalCount"]
                }
                prs.append(info)
            
            results.extend(prs)

    except Exception as e:
        print(f"\nErro durante a execução da consulta: {e}")
        print("Salvando itens encontrados até agora em arquivo CSV...\n")

    finally:
        end_time = time.time()
        print(f"{len(results) - current_results_len} Pull Requests encontrados")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
        print(f"Total de erros: {req_errors} ({req_errors / len(repos) * 100:.2f}%)")

        return results


def summarized_data(df: DataFrame): 
    metricas = {
        'Tamanho': ['Arquivos Alterados', 'Linhas Adicionadas', 'Linhas Excluídas'],
        'Tempo de Análise': ['Intervalo Criação e Última Atividade'],
        'Descrição': ['Caracteres Corpo PR'],
        'Interações': ['Participantes PR', 'Comentários PR']
    }

    colunas_numericas = []
    for metrica in metricas.values():
        colunas_numericas.extend(metrica)

    mediana_por_repo = df.groupby('Repositório')[colunas_numericas].median()
    mediana_por_repo = mediana_por_repo.round(2)
    mediana_por_repo.reset_index(inplace=True)
    
    media_por_repo = df.groupby('Repositório')[colunas_numericas].mean()
    media_por_repo.reset_index(inplace=True)
    media_por_repo = media_por_repo.round(2)
    
    resultados = pd.merge(mediana_por_repo, media_por_repo, on='Repositório', suffixes=(' (Mediana)', ' (Média)'))
    
    return resultados