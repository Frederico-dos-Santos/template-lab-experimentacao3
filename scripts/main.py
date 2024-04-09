from getData import get_repo_data, get_pr_data
from saveData import save_to_csv, read_csv, merge_data

def main():
    repo_results = read_csv("raw_repo_data.csv")
    if repo_results is None:
        repo_results = get_repo_data(num_repos=200, per_page=5)
        save_to_csv(repo_results, "raw_repo_data.csv")
    
    pr_results = read_csv("raw_pr_data.csv")
    if pr_results is None:
        pr_results = get_pr_data(repo_results)
        save_to_csv(pr_results, "raw_pr_data.csv")
    
    data_results = merge_data(repo_results, pr_results, column_join='Repositório')
    save_to_csv(data_results, "data.csv")

if __name__ == "__main__":
    main()