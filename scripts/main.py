import pandas as pd
from manipulateData import get_repo_data, get_pr_data, summarized_data, get_correlation_coefficient
from saveData import save_to_csv, read_csv, merge_data
from createGraphs import dispertion, bar

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
    df_changes_req = data_results[data_results["Status Revisão"] == "CHANGES_REQUESTED"]
    df_review_req = data_results[data_results["Status Revisão"] == "REVIEW_REQUIRED"]
        
    bar(
        colors=["#ad150a", "#d11f0f", "#f62a14"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Arquivos Alterados"].sum(), df_changes_req["Arquivos Alterados"].sum(), df_review_req["Arquivos Alterados"].sum()],
        value_label="Total de Arquivos Alterados",
        title="Correlação de Tamanho e Feedback final das Revisões"
    )
    bar(
        colors=["#ad150a", "#d11f0f", "#f62a14"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Arquivos Alterados"].mean(), df_changes_req["Arquivos Alterados"].mean(), df_review_req["Arquivos Alterados"].mean()],
        value_label="Média de Arquivos Alterados",
        title="Correlação de Tamanho e Feedback final das Revisões"
    )
    bar(
        colors=["#ad150a", "#d11f0f", "#f62a14"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Arquivos Alterados"].median(), df_changes_req["Arquivos Alterados"].median(), df_review_req["Arquivos Alterados"].median()],
        value_label="Mediana de Arquivos Alterados",
        title="Correlação de Tamanho e Feedback final das Revisões"
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
    
    bar(
        colors=["#429334", "#58a948", "#6fbf5d"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Linhas Adicionadas"].sum(), df_changes_req["Linhas Adicionadas"].sum(), df_review_req["Linhas Adicionadas"].sum()],
        value_label="Total de Linhas Adicionadas",
        title="Correlação de Tamanho e Feedback final das Revisões"
    )
    bar(
        colors=["#429334", "#58a948", "#6fbf5d"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Linhas Adicionadas"].mean(), df_changes_req["Linhas Adicionadas"].mean(), df_review_req["Linhas Adicionadas"].mean()],
        value_label="Média de Linhas Adicionadas",
        title="Correlação de Tamanho e Feedback final das Revisões"
    )
    bar(
        colors=["#429334", "#58a948", "#6fbf5d"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Linhas Adicionadas"].median(), df_changes_req["Linhas Adicionadas"].median(), df_review_req["Linhas Adicionadas"].median()],
        value_label="Mediana de Linhas Adicionadas",
        title="Correlação de Tamanho e Feedback final das Revisões"
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
    
    bar(
        colors=["#5230f4", "#7a4ff8", "#a26dfb"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Linhas Excluídas"].sum(), df_changes_req["Linhas Excluídas"].sum(), df_review_req["Linhas Excluídas"].sum()],
        value_label="Total de Linhas Excluídas",
        title="Correlação de Tamanho e Feedback final das Revisões"
    )
    bar(
        colors=["#5230f4", "#7a4ff8", "#a26dfb"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Linhas Excluídas"].mean(), df_changes_req["Linhas Excluídas"].mean(), df_review_req["Linhas Excluídas"].mean()],
        value_label="Média de Linhas Excluídas",
        title="Correlação de Tamanho e Feedback final das Revisões"
    )
    bar(
        colors=["#5230f4", "#7a4ff8", "#a26dfb"],
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Linhas Excluídas"].median(), df_changes_req["Linhas Excluídas"].median(), df_review_req["Linhas Excluídas"].median()],
        value_label="Mediana de Linhas Excluídas",
        title="Correlação de Tamanho e Feedback final das Revisões"
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
    
    bar(
        colors=["#ffc219", "#f07c19", "#e32551"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Intervalo Criação e Última Atividade"].sum(), df_changes_req["Intervalo Criação e Última Atividade"].sum(), df_review_req["Intervalo Criação e Última Atividade"].sum()],
        value_label="Total do Intervalo Criação e Última Atividade (em horas)",
        title="Correlação de Tempo de Análise e Feedback final das Revisões"
    )
    bar(
        colors=["#ffc219", "#f07c19", "#e32551"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Intervalo Criação e Última Atividade"].mean(), df_changes_req["Intervalo Criação e Última Atividade"].mean(), df_review_req["Intervalo Criação e Última Atividade"].mean()],
        value_label="Média do Intervalo Criação e Última Atividade (em horas)",
        title="Correlação de Tempo de Análise e Feedback final das Revisões"
    )
    bar(
        colors=["#ffc219", "#f07c19", "#e32551"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Intervalo Criação e Última Atividade"].median(), df_changes_req["Intervalo Criação e Última Atividade"].median(), df_review_req["Intervalo Criação e Última Atividade"].median()],
        value_label="Mediana do Intervalo Criação e Última Atividade (em horas)",
        title="Correlação de Tempo de Análise e Feedback final das Revisões"
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
        
    bar(
        colors=["#5015bd", "#027fe9", "#00caf8"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Caracteres Corpo PR"].sum(), df_changes_req["Caracteres Corpo PR"].sum(), df_review_req["Intervalo Criação e Última Atividade"].sum()],
        value_label="Total de Caracteres Corpo PR",
        title="Correlação de Descrição e Feedback final das Revisões"
    )
    bar(
        colors=["#5015bd", "#027fe9", "#00caf8"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Caracteres Corpo PR"].mean(), df_changes_req["Caracteres Corpo PR"].mean(), df_review_req["Intervalo Criação e Última Atividade"].mean()],
        value_label="Média de Caracteres Corpo PR",
        title="Correlação de Descrição e Feedback final das Revisões"
    )
    bar(
        colors=["#5015bd", "#027fe9", "#00caf8"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Caracteres Corpo PR"].median(), df_changes_req["Caracteres Corpo PR"].median(), df_review_req["Intervalo Criação e Última Atividade"].median()],
        value_label="Mediana de Caracteres Corpo PR",
        title="Correlação de Descrição e Feedback final das Revisões"
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
    
    bar(
        colors=["#a90448", "#fb3640", "#fda543"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Participantes PR"].sum(), df_changes_req["Participantes PR"].sum(), df_review_req["Participantes PR"].sum()],
        value_label="Total de Participantes PR",
        title="Correlação de Interações e Feedback final das Revisões"
    )
    
    bar(
        colors=["#a90448", "#fb3640", "#fda543"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Participantes PR"].mean(), df_changes_req["Participantes PR"].mean(), df_review_req["Participantes PR"].mean()],
        value_label="Média de Participantes PR",
        title="Correlação de Interações e Feedback final das Revisões"
    )
    
    bar(
        colors=["#a90448", "#fb3640", "#fda543"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Participantes PR"].median(), df_changes_req["Participantes PR"].median(), df_review_req["Participantes PR"].median()],
        value_label="Mediana de Participantes PR",
        title="Correlação de Interações e Feedback final das Revisões"
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
    
    bar(
        colors=["#07f9a2", "#0a8967", "#0d192b"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Comentários PR"].sum(), df_changes_req["Comentários PR"].sum(), df_review_req["Comentários PR"].sum()],
        value_label="Total de Comentários PR",
        title="Correlação de Interações e Feedback final das Revisões"
    )
    bar(
        colors=["#07f9a2", "#0a8967", "#0d192b"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Comentários PR"].mean(), df_changes_req["Comentários PR"].mean(), df_review_req["Comentários PR"].mean()],
        value_label="Média de Comentários PR",
        title="Correlação de Interações e Feedback final das Revisões"
    )
    bar(
        colors=["#07f9a2", "#0a8967", "#0d192b"], 
        bars=["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
        values=[df_approved["Comentários PR"].median(), df_changes_req["Comentários PR"].median(), df_review_req["Comentários PR"].median()],
        value_label="Mediana de Comentários PR",
        title="Correlação de Interações e Feedback final das Revisões"
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
    dispertion(
        novo_df,
        color="green", 
        columns={"x": "Arquivos Alterados", "y": "Revisões"},
        labels={"x": "Arquivos Alterados", "y": "Total de Revisões"},
        title="Correlação de Tamanho e Total de Revisões"
    )
    
    novo_df = data_summarized.loc[data_summarized['Linhas Adicionadas'] <= 10000]
    dispertion(
        novo_df,
        color="blue", 
        columns={"x": "Linhas Adicionadas", "y": "Revisões"},
        labels={"x": "Linhas Adicionadas", "y": "Total de Revisões"},
        title="Correlação de Tamanho e Total de Revisões"
    )
    
    novo_df = data_summarized.loc[data_summarized['Linhas Excluídas'] <= 4000]
    dispertion(
        novo_df,
        color="red", 
        columns={"x": "Linhas Excluídas", "y": "Revisões"},
        labels={"x": "Linhas Excluídas", "y": "Total de Revisões"},
        title="Correlação de Tamanho e Total de Revisões"
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
        title="Correlação de Tempo de Análise e Total de Revisões"
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
        title="Correlação de Descrição e Total de Revisões"
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
        title="Correlação de Interações e Total de Revisões"
    )

    dispertion(
        data_summarized,
        color="blue", 
        columns={"x": "Comentários PR", "y": "Revisões"},
        labels={"x": "Comentários do PR", "y": "Total de Revisões"},
        title="Correlação de Interações e Total de Revisões"
    )
    
    
if __name__ == "__main__":
    main()
