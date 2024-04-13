import json
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


def run_query(query, variables=None, max_retries=3):
    retries = 0
    while retries < max_retries:
        response = requests.post(
            API_URL, json={"query": query, "variables": variables}, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            retries += 1
            if retries == 1:
                print()
                
            print(f"Retentativa {retries} após erro {response.status_code}.")
            time.sleep(5)
    raise Exception(f"Query failed after multiple retries: {json.loads(response.text)['errors'][0]['message']}")


def get_repo_data(num_repos: int, per_page: int, results: list=[]) -> list:
    print(f"Buscando {num_repos} repositórios...")
    start_time = time.time()

    cursor: str = None
    has_next_page: bool = True
    current_results_len = len(results)

    if results is None:
        results = list()
    else:
        cursor = results[-1]["next_cursor"]

    try:
        while len(results) < num_repos and has_next_page:
            variables = {
                "perPage": per_page,
                "cursor": cursor
            }

            data = run_query(query=repo_query, variables=variables)

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
                    "current_cursor": cursor,
                    "next_cursor": data["data"]["search"]["pageInfo"]["endCursor"]
                }
                results.append(result_info)

            has_next_page = data["data"]["search"]["pageInfo"]["hasNextPage"]
            if not has_next_page:
                break
            
            time.sleep(1)

    except Exception as e:
        print(f"\nErro durante a execução da consulta: {e}")
        print("Salvando itens encontrados até agora em arquivo CSV...\n")

    finally:
        end_time = time.time()
        print(f"{len(results) - current_results_len} repositórios encontrados")
        print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")

    return results


def get_pr_data(repos: list, results: list=[]) -> list:
    print("Buscando informações dos Pull Requests...")
    start_time = time.time()

    current_results_len = len(results)
    if results is None:
        results = list()
        
    try:
        for repo in repos:
            existe = any(repo["Repositório"] == result["Repositório"]
                         for result in results)
            if existe:
                continue

            owner, repo_name = repo["Repositório"].split("/")
            pr_variables = {"owner": owner, "name": repo_name}
            data = run_query(query=pr_query, variables=pr_variables)

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
            time.sleep(65)

    except Exception as e:
        print(f"\nErro durante a execução da consulta: {e}")
        print("Salvando itens encontrados até agora em arquivo CSV...\n")
        return results

    finally:
        end_time = time.time()
        print(f"{len(results) - current_results_len} Pull Requests encontrados")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")

    return results


def summarized_data(df: DataFrame): 
    results = []
    repos = df.groupby('Repositório')

    for nome_repo, grupo_repo in repos:
        lista_repo = grupo_repo.values.tolist()
        df_repos = DataFrame(lista_repo, columns=grupo_repo.columns)
        grouped = df_repos.groupby('Estado PR')

        for name, group in grouped:
            print(f'Grupo: {name}')
            print(group)
            print()
            
        tamanho_feedback_revisao = df_repos.groupby('Estado PR')['Número PR'].mean()
        
        df_repos['Data de Criação PR'] = pd.to_datetime(df_repos['Data de Criação PR'])
        df_repos['Data de Fechamento PR'] = pd.to_datetime(df_repos['Data de Fechamento PR'])
        df_repos['Tempo de Análise (horas)'] = (df_repos['Data de Fechamento PR'] - df_repos['Data de Criação PR']).dt.total_seconds() / 3600
        tempo_analise_feedback_revisao = df_repos.groupby('Estado PR')['Tempo de Análise (horas)'].mean()
        
        tamanho_descricao_feedback_revisao = df_repos.groupby('Estado PR')['Caracteres Corpo PR'].mean()
        interacoes_feedback_revisao = df_repos.groupby('Estado PR')['Participantes PR', 'Comentários PR'].mean()
        tamanho_numero_revisoes = df_repos.groupby('Revisões')['Tamanho PRs'].mean()
        tempo_analise_numero_revisoes = df_repos.groupby('Revisões')['Tempo de Análise (horas)'].mean()
        tamanho_descricao_numero_revisoes = df_repos.groupby('Revisões')['Caracteres Corpo PR'].mean()
        interacoes_numero_revisoes = df_repos.groupby('Revisões')['Participantes PR', 'Comentários PR'].mean()
        
        metrics = {
            "Repositório": nome_repo,
            "Tamanho PRs (Feedback/Revisão)": tamanho_feedback_revisao,
            "Tempo de Análise (horas) (Feedback/Revisão)": tempo_analise_feedback_revisao,
            "Tamanho Descrição (Feedback/Revisão)": tamanho_descricao_feedback_revisao,
            "Interacoes (Feedback/Revisão)": interacoes_feedback_revisao,
            "Tamanho PRs (Número de Revisões)": tamanho_numero_revisoes,
            "Tempo de Análise (horas) (Número de Revisões)": tempo_analise_numero_revisoes,
            "Tamanho Descrição (Número de Revisões)": tamanho_descricao_numero_revisoes,
            "Interacoes (Número de Revisões)": interacoes_numero_revisoes
        }
        
        results.append(metrics)
    
    return results