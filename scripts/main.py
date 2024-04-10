from getData import get_repo_data, get_pr_data
from saveData import save_to_csv, read_csv, merge_data

NUM_REPOSTORIES = 200
PER_PAGE = 10

def main():
    repo_results = read_csv("raw_repo_data.csv")
    if repo_results is None or len(repo_results) < NUM_REPOSTORIES:
        repo_results = get_repo_data(
            num_repos=NUM_REPOSTORIES, per_page=PER_PAGE, results=repo_results)
        save_to_csv(repo_results, "raw_repo_data.csv")

    pr_results = read_csv("raw_pr_data.csv")
    if pr_results is None or len(repo_results) < NUM_REPOSTORIES * 100:
        pr_results = get_pr_data(repos=repo_results, results=pr_results)
        save_to_csv(pr_results, "raw_pr_data.csv")

    # repo_results = read_csv("raw_repo_data.csv", columns=["Repositório", "Estrelas", "Pull Requests"])
    # data_results = merge_data(repo_results, pr_results,
    #                           column_join='Repositório')
    # if data_results is not None:
    #     save_to_csv(data_results, "data.csv")


if __name__ == "__main__":
    main()
