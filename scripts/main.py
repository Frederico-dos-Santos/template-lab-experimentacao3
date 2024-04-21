import pandas as pd
from manipulateData import get_repo_data, get_pr_data, summarized_data, get_correlation_coefficient
from saveData import save_to_csv, read_csv, merge_data
from createGraphs import dispertion, violin

NUM_REPOSTORIES = 250
PER_PAGE = 1

def main():
    # repo_results = read_csv("raw_repo_data.csv")
    # if repo_results is None or len(repo_results) < NUM_REPOSTORIES:
    #     repo_results = get_repo_data(
    #         num_repos=NUM_REPOSTORIES, per_page=PER_PAGE, results=repo_results if repo_results is not None else [])
    #     save_to_csv(repo_results, "raw_repo_data.csv")
        
    pr_results = read_csv("raw_pr_data.csv")
    # if pr_results is None or len(pr_results) < NUM_REPOSTORIES:
    #     pr_results = get_pr_data(repo_results=repo_results, pr_results=pr_results if pr_results is not None else [], per_page=PER_PAGE)
    #     save_to_csv(pr_results, "raw_pr_data.csv")

    repo_results = read_csv("raw_repo_data.csv", columns=['Repositório', 'Estrelas', 'Pull Requests'])
    data_results = merge_data(repo_results, pr_results,
                              column_join='Repositório')
    if data_results is not None:
        save_to_csv(data_results, "data.csv")
    
    metrics = ['Intervalo Criação e Última Atividade', 'Caracteres Corpo PR']
    data_summarized = summarized_data(data_results, columns=metrics)
    if data_summarized is not None:
        save_to_csv(data_summarized, "data_summarized.csv")
    
    data_summarized = read_csv("data_summarized.csv", "dataframe")

    # RQ 01 - Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Arquivos Alterados", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Arquivos Alterados", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Arquivos Alterados", "REVIEW_REQUIRED"])

    print("Arquivos Alterados x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nArquivos Alterados x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nArquivos Alterados x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
        
    df_approved = data_results[data_results["Status Revisão"] == "APPROVED"]
    data_analysis_approved = df_approved.groupby("Repositório")[["Arquivos Alterados", "Linhas Adicionadas", "Linhas Excluídas"]].mean().fillna(0)
    
    df_changes_req = data_results[data_results["Status Revisão"] == "CHANGES_REQUESTED"]
    data_analysis_changes_req = df_changes_req.groupby("Repositório")[["Arquivos Alterados", "Linhas Adicionadas", "Linhas Excluídas"]].mean().fillna(0)
    
    df_review_req = data_results[data_results["Status Revisão"] == "REVIEW_REQUIRED"]
    data_analysis_review_req = df_review_req.groupby("Repositório")[["Arquivos Alterados", "Linhas Adicionadas", "Linhas Excluídas"]].mean().fillna(0)
    
    novo_df = data_analysis_approved[data_analysis_approved['Arquivos Alterados'] <= 50]
    violin(
        novo_df,
        column="Arquivos Alterados",
        title="Correlação de Arquivos Alterados (Média) e Revisões Aprovadas"
    )
    
    
    novo_df = data_analysis_changes_req[data_analysis_changes_req['Arquivos Alterados'] <= 50]
    violin(
        novo_df,
        column="Arquivos Alterados",
        title="Correlação de Arquivos Alterados (Média) e Revisões Mudanças Pendentes"
    )
    
    
    novo_df = data_analysis_review_req[data_analysis_review_req['Arquivos Alterados'] <= 150]
    violin(
        novo_df,
        column="Arquivos Alterados",
        title="Correlação de Arquivos Alterados (Média) e Revisões Necessárias"
    )
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "REVIEW_REQUIRED"])
    
    print("\n\nLinhas Adicionadas x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nLinhas Adicionadas x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nLinhas Adicionadas x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
    novo_df = data_analysis_approved[data_analysis_approved['Linhas Adicionadas'] <= 2000]
    violin(
        novo_df,
        column="Linhas Adicionadas",
        title="Correlação de Linhas Adicionadas (Média) e Revisões Aprovadas"
    )
    
    novo_df = data_analysis_changes_req[data_analysis_changes_req['Linhas Adicionadas'] <= 1500]
    violin(
        novo_df,
        column="Linhas Adicionadas",
        title="Correlação de Linhas Adicionadas (Média) e Revisões Mudanças Pendentes"
    )
    
    novo_df = data_analysis_review_req[data_analysis_review_req['Linhas Adicionadas'] <= 1500]
    violin(
        novo_df,
        column="Linhas Adicionadas",
        title="Correlação de Linhas Adicionadas (Média) e Revisões Necessárias"
    )
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "REVIEW_REQUIRED"])
    
    print("\n\nLinhas Excluídas x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nLinhas Excluídas x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nLinhas Excluídas x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
    novo_df = data_analysis_approved[data_analysis_approved['Linhas Excluídas'] <= 700]
    violin(
        novo_df,
        column="Linhas Excluídas",
        title="Correlação de Linhas Excluídas (Média) e Revisões Aprovadas"
    )
    
    novo_df = data_analysis_changes_req[data_analysis_changes_req['Linhas Excluídas'] <= 500]
    violin(
        novo_df,
        column="Linhas Excluídas",
        title="Correlação de Linhas Excluídas (Média) e Revisões Mudanças Pendentes"
    )
    
    novo_df = data_analysis_review_req[data_analysis_review_req['Linhas Excluídas'] <= 1500]
    violin(
        novo_df,
        column="Linhas Excluídas",
        title="Correlação de Linhas Excluídas (Média) e Revisões Necessárias"
    )
    
    # RQ 02 - Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "REVIEW_REQUIRED"])

    print("\n============================================================")
    print("\nIntervalo Criação e Última Atividade x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nIntervalo Criação e Última Atividade x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nIntervalo Criação e Última Atividade x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
    dispertion(
        data_summarized,
        columns={"x": "Intervalo Criação e Última Atividade", "y": "APPROVED"},
        color="red", 
        labels={"x": "Intervalo Médio de Análise (em horas)", "y": "Quantidade de PRs Aprovados"},
        title="Correlação de Tempo de Análise e Revisões Aprovadas"
    )
    
    dispertion(
        data_summarized,
        color="green", 
        columns={"x": "Intervalo Criação e Última Atividade", "y": "CHANGES_REQUESTED"},
        labels={"x": "Intervalo Médio de Análise (em horas)", "y": "Quantidade de PRs com Mudanças Pendentes"},
        title="Correlação de Tempo de Análise e Revisões com Mudanças Pendentes"
    )
    
    dispertion(
        data_summarized,
        color="gray", 
        columns={"x": "Intervalo Criação e Última Atividade", "y": "REVIEW_REQUIRED"},
        labels={"x": "Intervalo Médio de Análise (em horas)", "y": "Quantidade de PRs com Revisão Necessária"},
        title="Correlação de Tempo de Análise e Revisões Necessárias"
    )
    
    # RQ 03 - Qual a relação entre a descrição dos PRs e o feedback final das revisões?
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "REVIEW_REQUIRED"])
    
    print("\n============================================================")
    print("\nCaracteres do Corpo do PR x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nCaracteres do Corpo do PR x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nCaracteres do Corpo do PR x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
    # Remover outilers (Caracteres Corpo PR < 1000)
    novo_df = data_summarized.loc[data_summarized['Caracteres Corpo PR'] <= 1000]
    dispertion(
        novo_df,
        color="purple", 
        columns={"x": "Caracteres Corpo PR", "y": "APPROVED"},
        labels={"x": "Quantidade de caracteres do Corpo do PR", "y": "Quantidade de PRs Aprovados"},
        title="Correlação de Descrição e Revisões Aprovadas"
    )
    
    # Remover outliers (Caracteres Corpo PR < 1000; feedback < 12)
    novo_df = data_summarized.loc[data_summarized['Caracteres Corpo PR'] <= 1000]
    novo_df = data_summarized.loc[data_summarized['CHANGES_REQUESTED'] <= 12]
    dispertion(
        novo_df,
        color="orange", 
        columns={"x": "Caracteres Corpo PR", "y": "CHANGES_REQUESTED"},
        labels={"x": "Quantidade de caracteres do Corpo do PR", "y": "Quantidade de PRs com Mudanças Pendentes"},
        title="Correlação de Descrição e Revisões com Mudanças Pendentes"
    )
    
    # Remover outliers (Caracteres Corpo PR < 1000; feedback < 40)
    novo_df = data_summarized.loc[data_summarized['Caracteres Corpo PR'] <= 1000]
    novo_df = data_summarized.loc[data_summarized['REVIEW_REQUIRED'] <= 40]
    dispertion(
        novo_df,
        color="blue", 
        columns={"x": "Caracteres Corpo PR", "y": "REVIEW_REQUIRED"},
        labels={"x": "Quantidade de caracteres do Corpo do PR", "y": "Quantidade de PRs com Revisão Necessária"},
        title="Correlação de Descrição e Revisões Necessárias"
    )
    
    # RQ 04 - Qual a relação entre as interações nos PRs e o feedback final das revisões?
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "REVIEW_REQUIRED"])

    print("\n============================================================")
    print("\nParticipantes do PR x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nParticipantes do PR x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nParticipantes do PR x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
    # Usar violin
    data_analysis_approved = df_approved.groupby("Repositório")[["Comentários PR", "Participantes PR"]].sum().fillna(0)
    violin(
        data_analysis_approved,
        column="Participantes PR",
        title="Correlação de Participantes do PR e Revisões Aprovadas"
    )
    
    data_analysis_changes_req = df_changes_req.groupby("Repositório")[["Comentários PR", "Participantes PR"]].sum().fillna(0)
    violin(
        data_analysis_changes_req,
        column="Participantes PR",
        title="Correlação de Participantes do PR e Revisões com Mudanças Pendentes"
    )
    
    data_analysis_review_req = df_review_req.groupby("Repositório")[["Comentários PR", "Participantes PR"]].sum().fillna(0)
    violin(
        data_analysis_review_req,
        column="Participantes PR",
        title="Correlação de Participantes do PR e Revisões Necessárias"
    )
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "REVIEW_REQUIRED"])

    print("\n\Comentários do PR x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\Comentários do PR x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\Comentários do PR x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")

    violin(
        data_analysis_approved,
        column="Comentários PR",
        title="Correlação de Comentários do PR e Revisões Aprovadas"
    )
    
    violin(
        data_analysis_changes_req,
        column="Comentários PR",
        title="Correlação de Comentários do PR e Revisões com Mudanças Pendentes"
    )

    novo_df = data_analysis_review_req[data_analysis_review_req['Comentários PR'] <= 200]
    violin(
        novo_df,
        column="Comentários PR",
        title="Correlação de Comentários do PR e Revisões Necessárias"
    )

    # RQ 05 - Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
    
    cc_arq_alterados, pv_arq_alterados = get_correlation_coefficient(
        data_summarized, columns=["Arquivos Alterados", "Revisões"])
    cc_add_lines, pv_add_lines = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "Revisões"])
    cc_del_lines, pv_del_lines = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "Revisões"])

    print("\n============================================================")
    print("\nArquivos Alterados x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_arq_alterados}")
    print(f"P_value: {pv_arq_alterados}")
    
    print("\n\nLinhas Adicionadas x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_add_lines}")
    print(f"P_value: {pv_add_lines}")
    
    print("\n\nLinhas Excluídas x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_del_lines}")
    print(f"P_value: {pv_del_lines}")
    
    novo_df = data_summarized.loc[data_summarized['Arquivos Alterados'] <= 5000]
    novo_df = data_summarized.loc[data_summarized['Linhas Adicionadas'] <= 10000]
    novo_df = data_summarized.loc[data_summarized['Linhas Excluídas'] <= 4000]
    dispertion(
        novo_df,
        color="green", 
        columns={"x": "Arquivos Alterados", "y": "Revisões"},
        labels={"x": "Arquivos Alterados", "y": "Total de Revisões"},
        title="Correlação de Arquivos Alterados e Total de Revisões"
    )
    
    dispertion(
        novo_df,
        color="blue", 
        columns={"x": "Linhas Adicionadas", "y": "Revisões"},
        labels={"x": "Linhas Adicionadas", "y": "Total de Revisões"},
        title="Correlação de Linhas Adicionadas e Total de Revisões"
    )
    
    dispertion(
        novo_df,
        color="red", 
        columns={"x": "Linhas Excluídas", "y": "Revisões"},
        labels={"x": "Linhas Excluídas", "y": "Total de Revisões"},
        title="Correlação de Linhas Excluídas e Total de Revisões"
    )
    
    # RQ 06 - Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
    
    cc_interval, pv_interval = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "Revisões"])

    print("\n============================================================")
    print("\nIntervalo Criação e Última Atividade x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_interval}")
    print(f"P_value: {pv_interval}")
    
    # Remover Outliers (Intervalo < 1000)
    dispertion(
        data_summarized,
        color="purple", 
        columns={"x": "Revisões", "y": "Intervalo Criação e Última Atividade"},
        labels={"x": "Total de Revisões", "y": "Intervalo Criação e Última Atividade"},
        title="Correlação de Intervalo de Criação e Última Atividade e Revisões"
    )
    
    # RQ 07 - Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "Revisões"])

    print("\n============================================================")
    print("\nCaracteres Corpo PR x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    # Remover Outliers (Caracteres Corpo < 1000)
    dispertion(
        data_summarized,
        color="orange", 
        columns={"x": "Revisões", "y": "Caracteres Corpo PR"},
        labels={"x": "Total de Revisões", "y": "Caracteres no Corpo PR"},
        title="Correlação de Quantidade de caracteres no Corpo do PR e Revisões"
    )
    
    # RQ 08 - Qual a relação entre as interações nos PRs e o número de revisões realizadas?

    cc_participantes, pv_participantes = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "Revisões"])
    cc_comments, pv_comments = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "Revisões"])

    print("\n============================================================")
    print("\nParticipantes do PR x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_participantes}")
    print(f"P_value: {pv_participantes}")
    
    print("\n\nComentários do PR x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_comments}")
    print(f"P_value: {pv_comments}")
    
    dispertion(
        data_summarized,
        color="red", 
        columns={"x": "Participantes PR", "y": "Revisões"},
        labels={"x": "Participantes do PR", "y": "Total de Revisões"},
        title="Correlação de Quantidade de Participantes do PR e Total de Revisões"
    )

    dispertion(
        data_summarized,
        color="blue", 
        columns={"x": "Comentários PR", "y": "Revisões"},
        labels={"x": "Comentários do PR", "y": "Total de Revisões"},
        title="Correlação de Quantidade de Comentários do PR e Total de Revisões"
    )
    
    
if __name__ == "__main__":
    main()
