from manipulateData import get_repo_data, get_pr_data, summarized_data, get_correlation_coefficient
from saveData import save_to_csv, read_csv, merge_data
from createGraphs import dispertion, bar, boxplot

NUM_REPOSTORIES = 200
PER_PAGE = 1

def main():
    repo_results = read_csv("raw_repo_data.csv")
    # if repo_results is None or len(repo_results) < NUM_REPOSTORIES:
    #     repo_results = get_repo_data(
    #         num_repos=NUM_REPOSTORIES, per_page=PER_PAGE, results=repo_results if repo_results is not None else [])
    #     save_to_csv(repo_results, "raw_repo_data.csv")
        
    pr_results = read_csv("raw_pr_data.csv")
    # if pr_results is None or len(pr_results) < NUM_REPOSTORIES * 100:
    #     pr_results = get_pr_data(repo_results=repo_results, pr_results=pr_results if pr_results is not None else [])
    #     save_to_csv(pr_results, "raw_pr_data.csv")

    repo_results = read_csv("raw_repo_data.csv", columns=['Repositório', 'Estrelas', 'Pull Requests'])
    data_results = merge_data(repo_results, pr_results,
                              column_join='Repositório')
    if data_results is not None:
        save_to_csv(data_results, "data.csv")
    
    mean_metrics = ['Intervalo Criação e Última Atividade', 'Participantes PR', 'Caracteres Corpo PR']
    total_metrics = ['Revisões', 'Comentários PR', 'Arquivos Alterados', 'Linhas Adicionadas', 'Linhas Excluídas']
    data_summarized = summarized_data(data_results, mean_columns=mean_metrics, total_columns=total_metrics)
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
    df_changes_req = data_results[data_results["Status Revisão"] == "CHANGES_REQUESTED"]
    df_review_req = data_results[data_results["Status Revisão"] == "REVIEW_REQUIRED"]
    
    metrics_sum = ["Arquivos Alterados", "Linhas Adicionadas", "Linhas Excluídas", "Caracteres Corpo PR"]
    novo_df_approved = df_approved.groupby("Repositório")[metrics_sum].sum().reset_index()
    novo_df_changes_req = df_changes_req.groupby("Repositório")[metrics_sum].sum().reset_index()
    novo_df_review_req = df_review_req.groupby("Repositório")[metrics_sum].sum().reset_index()
    
    boxplot(
        data=[novo_df_approved['Arquivos Alterados'], novo_df_changes_req['Arquivos Alterados'], novo_df_review_req['Arquivos Alterados']],
        columns=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        x_label="Feedback final das Revisões",
        y_label="Total de Arquivos Alterados",
        title="Correlação entre Arquivos Alterados e Feedback final das Revisões",
        range=(-100, 1000)
    )
    
    boxplot(
        data=novo_df_changes_req['Arquivos Alterados'],
        columns=["CHANGES_REQUESTED"],
        x_label="Revisões com Mudanças Requisitada",
        y_label="Total de Arquivos Alterados",
        title="Correlação entre Arquivos Alterados e Revisões com Mudanças Requisitadas",
        range=(-5, 50)
    )
    
    print("\n=======================================")
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "REVIEW_REQUIRED"])

    
    print("\nLinhas Adicionadas x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nLinhas Adicionadas x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nLinhas Adicionadas x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
    filtered_df_approved = novo_df_approved[novo_df_approved['Linhas Adicionadas'] <= 5000]
    filtered_df_review_req = novo_df_review_req[novo_df_review_req['Linhas Adicionadas'] <= 5000]
    
    boxplot(
        data=[filtered_df_approved['Linhas Adicionadas'], novo_df_changes_req['Linhas Adicionadas'], filtered_df_review_req['Linhas Adicionadas']],
        columns=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        x_label="Feedback final das Revisões",
        y_label="Total de Linhas Adicionadas",
        title="Correlação entre Linhas Adicionadas e Feedback final das Revisões",
        range=(-100, 5000)
    )
    
    filtered_df_changes_req = novo_df_changes_req[novo_df_changes_req['Linhas Adicionadas'] <= 250]
    boxplot(
        filtered_df_changes_req['Linhas Adicionadas'],
        columns=["CHANGES_REQUESTED"],
        x_label="Revisões com Mudanças Requisitadas",
        y_label="Total de Linhas Adicionadas",
        title="Correlação entre Linhas Adicionadas e Revisões com Mudanças Requisitadas",
        range=(-10, 250)
    )
    
    print("\n=======================================")
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "REVIEW_REQUIRED"])
    
    print("\nLinhas Excluídas x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nLinhas Excluídas x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nLinhas Excluídas x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
  
    filtered_df_approved = novo_df_approved[novo_df_approved['Linhas Excluídas'] <= 2000]
    filtered_df_review_req = novo_df_review_req[novo_df_review_req['Linhas Excluídas'] <= 2000]
    boxplot(
        data=[filtered_df_approved['Linhas Excluídas'], novo_df_changes_req['Linhas Excluídas'], filtered_df_review_req['Linhas Excluídas']],
        columns=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        x_label="Feedback final das Revisões",
        y_label="Total de Linhas Excluídas",
        title="Correlação entre Linhas Excluídas e Feedback final das Revisões",
        range=(-100, 2000)
    )
    
    filtered_df_changes_req = novo_df_changes_req[novo_df_changes_req['Linhas Excluídas'] <= 15]
    boxplot(
        filtered_df_changes_req['Linhas Excluídas'],
        columns=["CHANGES_REQUESTED"],
        x_label="Revisões com Mudanças Requisitadas",
        y_label="Total de Linhas Excluídas",
        title="Correlação entre Linhas Excluídas e Revisões com Mudanças Requisitadas",
        range=(-5, 15)
    )
    
    # RQ 02 - Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
    print("\n============================================================")
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "REVIEW_REQUIRED"])
    
    print("\nIntervalo Criação e Última Atividade x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nIntervalo Criação e Última Atividade x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nIntervalo Criação e Última Atividade x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")

    metrics_mean = ["Intervalo Criação e Última Atividade", "Participantes PR", "Comentários PR"]
    df_approved_mean = df_approved.groupby("Repositório")[metrics_mean].mean().reset_index()
    df_changes_req_mean = df_changes_req.groupby("Repositório")[metrics_mean].mean().reset_index()
    df_review_req_mean = df_review_req.groupby("Repositório")[metrics_mean].mean().reset_index()
    
    boxplot(
        data=[df_approved_mean['Intervalo Criação e Última Atividade'], df_changes_req_mean['Intervalo Criação e Última Atividade'], df_review_req_mean['Intervalo Criação e Última Atividade']],
        columns=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        x_label="Feedback final das Revisões",
        y_label="Intervalo Criação e Última Atividade",
        title="Correlação entre Intervalo Criação e Última Atividade e Feedback final das Revisões",
        range=(-100, 2500)
    )

    boxplot(
        data=[df_approved_mean['Intervalo Criação e Última Atividade'], df_review_req_mean['Intervalo Criação e Última Atividade']],
        columns=["APPROVED", "REVIEW_REQUIRED"],
        x_label="Revisões Aprovadas e com Mudanças Requisitadas",
        y_label="Intervalo Criação e Última Atividade (Média)",
        title="Correlação entre Intervalo Criação e Última Atividade e Revisões Aprovadas e com Mudanças Requisitadas",
        range=(-50, 600)
    )
    
    
    # RQ 03 - Qual a relação entre a descrição dos PRs e o feedback final das revisões?
    print("\n============================================================")
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "REVIEW_REQUIRED"])
    
    print("\nCaracteres do Corpo do PR x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nCaracteres do Corpo do PR x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nCaracteres do Corpo do PR x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
        
    filtered_df_approved = novo_df_approved[novo_df_approved['Caracteres Corpo PR'] <= 10000]
    filtered_df_review_req = novo_df_review_req[novo_df_review_req['Caracteres Corpo PR'] <= 10000]
    boxplot(
        data=[filtered_df_approved['Caracteres Corpo PR'], novo_df_changes_req['Caracteres Corpo PR'], filtered_df_review_req['Caracteres Corpo PR']],
        columns=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        x_label="Feedback final das Revisões",
        y_label="Total de Caracteres Corpo PR",
        title="Correlação entre Caracteres Corpo PR e Feedback final das Revisões",
        range=(-100, 10000)
    )
    
    boxplot(
        data=[novo_df_changes_req['Caracteres Corpo PR']],
        columns=["CHANGES_REQUESTED"],
        x_label="Revisões com Mudanças Requisitadas",
        y_label="Total de Caracteres Corpo PR",
        title="Correlação entre Caracteres Corpo PR e Revisões com Mudanças Requisitadas",
        range=(-100, 5000)
    )
    
    # RQ 04 - Qual a relação entre as interações nos PRs e o feedback final das revisões?
    print("\n============================================================")
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "REVIEW_REQUIRED"])
    
    print("\nParticipantes do PR x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nParticipantes do PR x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nParticipantes do PR x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
      
    boxplot(
        data=[df_approved_mean['Participantes PR'], df_changes_req_mean['Participantes PR'], df_review_req_mean['Participantes PR']],
        columns=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        x_label="Feedback final das Revisões",
        y_label="Participantes do PR (Média)",
        title="Correlação entre Participantes do PR e Feedback final das Revisões",
        range=(0, 10)
    )
    
    print("\n=======================================")
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "APPROVED"])
    cc_changes_req, pv_changes_req = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "CHANGES_REQUESTED"])
    cc_review_req, pv_review_req = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "REVIEW_REQUIRED"])
    
    print("\nComentários do PR x APPROVED")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    print("\n\nComentários do PR x CHANGES_REQUESTED")
    print(f"\nCoeficiente de Correlação: {cc_changes_req}")
    print(f"P_value: {pv_changes_req}")
    
    print("\n\nComentários do PR x REVIEW_REQUIRED")
    print(f"\nCoeficiente de Correlação: {cc_review_req}")
    print(f"P_value: {pv_review_req}")
    
    boxplot(
        data=[df_approved_mean['Comentários PR'], df_changes_req_mean['Comentários PR'], df_review_req_mean['Comentários PR']],
        columns=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        x_label="Feedback final das Revisões",
        y_label="Comentários do PR (Média)",
        title="Correlação entre Comentários do PR e Feedback final das Revisões",
        range=(-1, 10)
    )

    # RQ 05 - Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
    print("\n============================================================")
    
    cc_arq_alterados, pv_arq_alterados = get_correlation_coefficient(
        data_summarized, columns=["Arquivos Alterados", "Revisões"])
    cc_add_lines, pv_add_lines = get_correlation_coefficient(
        data_summarized, columns=["Linhas Adicionadas", "Revisões"])
    cc_del_lines, pv_del_lines = get_correlation_coefficient(
        data_summarized, columns=["Linhas Excluídas", "Revisões"])

    print("\nArquivos Alterados x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_arq_alterados}")
    print(f"P_value: {pv_arq_alterados}")
    
    print("\n\nLinhas Adicionadas x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_add_lines}")
    print(f"P_value: {pv_add_lines}")
    
    print("\n\nLinhas Excluídas x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_del_lines}")
    print(f"P_value: {pv_del_lines}")
    
    dispertion(
        data_summarized,
        color="green", 
        columns={"x": "Arquivos Alterados", "y": "Revisões"},
        labels={"x": "Arquivos Alterados", "y": "Total de Revisões"},
        title="Correlação entre Tamanho e Total de Revisões",
        range=(0, 5000)
    )
    dispertion(
        data_summarized,
        color="blue", 
        columns={"x": "Linhas Adicionadas", "y": "Revisões"},
        labels={"x": "Linhas Adicionadas", "y": "Total de Revisões"},
        title="Correlação entre Tamanho e Total de Revisões",
        range=(0, 10000)
    )
    dispertion(
        data_summarized,
        color="red", 
        columns={"x": "Linhas Excluídas", "y": "Revisões"},
        labels={"x": "Linhas Excluídas", "y": "Total de Revisões"},
        title="Correlação entre Tamanho e Total de Revisões",
        range=(0, 4000)
    )
    
    # RQ 06 - Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
    print("\n============================================================")
    
    cc_interval, pv_interval = get_correlation_coefficient(
        data_summarized, columns=["Intervalo Criação e Última Atividade", "Revisões"])

    print("\nIntervalo Criação e Última Atividade x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_interval}")
    print(f"P_value: {pv_interval}")
    
    dispertion(
        data_summarized,
        color="purple", 
        columns={"x": "Revisões", "y": "Intervalo Criação e Última Atividade"},
        labels={"x": "Total de Revisões", "y": "Intervalo Criação e Última Atividade"},
        title="Correlação entre Tempo de Análise e Total de Revisões"
    )
    
    # RQ 07 - Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
    print("\n============================================================")
    
    cc_approved, pv_approved = get_correlation_coefficient(
        data_summarized, columns=["Caracteres Corpo PR", "Revisões"])

    print("\nCaracteres Corpo PR x Revisões")
    print(f"\nCoeficiente de Correlação: {cc_approved}")
    print(f"P_value: {pv_approved}")
    
    dispertion(
        data_summarized,
        color="orange", 
        columns={"x": "Revisões", "y": "Caracteres Corpo PR"},
        labels={"x": "Total de Revisões", "y": "Caracteres no Corpo PR"},
        title="Correlação entre Descrição e Total de Revisões"
    )
    
    # RQ 08 - Qual a relação entre as interações nos PRs e o número de revisões realizadas?

    print("\n============================================================")
    
    cc_participantes, pv_participantes = get_correlation_coefficient(
        data_summarized, columns=["Participantes PR", "Revisões"])
    cc_comments, pv_comments = get_correlation_coefficient(
        data_summarized, columns=["Comentários PR", "Revisões"])

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
        title="Correlação entre Interações e Total de Revisões"
    )

    dispertion(
        data_summarized,
        color="blue", 
        columns={"x": "Comentários PR", "y": "Revisões"},
        labels={"x": "Comentários do PR", "y": "Total de Revisões"},
        title="Correlação entre Interações e Total de Revisões"
    )
    
    
if __name__ == "__main__":
    main()
