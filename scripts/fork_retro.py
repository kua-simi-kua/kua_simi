from github import Github
from github import Auth
from argparse import ArgumentParser
import os
import pandas as pd

from utils import json_helper
from metadata_stats import REPOS_INFO_METADATA_PATH

def repos_string_target_forks(repos_info_file):
    repos_info_filename_noext = os.path.splitext(repos_info_file)[0]
    target_repo_string_tokens = repos_info_filename_noext[:-11]
    repos_info_filepath = REPOS_INFO_METADATA_PATH + target_repo_string_tokens + '/' + repos_info_file

    target_repo_string_tokens_list = target_repo_string_tokens.split("___")
    target_repo_string = target_repo_string_tokens_list[0] + '/' + target_repo_string_tokens_list[1]

    target_repo_metadata_dict = json_helper.read_json(repos_info_filepath)
    forkers_list = target_repo_metadata_dict.get("forkers")
    forked_repos_list = [forker + '/' + target_repo_string_tokens_list[1] for forker in forkers_list]

    return target_repo_string, forked_repos_list

def get_commit_info_list(repo_obj):
    return [
         (
            commit.sha,
            commit.commit.committer.date.strftime("%Y-%m-%d %H:%M:%S UTC"), 
            commit.html_url
          ) 
            for commit in repo_obj.get_commits()]

def compare_target_forked_commits(target_commit_info_list, forked_commit_info_list):
    common_commits = list()
    target_commit_info_list_copy = target_commit_info_list.copy()
    while len(target_commit_info_list_copy) and len(forked_commit_info_list):
        earliest_target_commit = target_commit_info_list_copy.pop()
        earliest_forked_commit = forked_commit_info_list.pop()
        if earliest_target_commit[0] != earliest_forked_commit[0]:
            target_commit_info_list_copy.append(earliest_target_commit)
            forked_commit_info_list.append(earliest_forked_commit)
            break
        common_commits.append(earliest_forked_commit)

    if not len(common_commits): # sometimes there are no common commit sha, could be rebased
        common_commits.append(forked_commit_info_list[-1])
    
    return len(target_commit_info_list_copy), len(forked_commit_info_list), common_commits[-1]



def main():
    argparser = ArgumentParser(description="Examine forks of a given repo")
    argparser.add_argument("repo_string", help="user_login/repo_name")
    args = argparser.parse_args()

    target_repo_string = args.repo_string
    
    with open("../config/github_auth_super.pass", "r") as pass_file: # ensure that this file is not committed/pushed
            auth_token_raw = pass_file.read()
            auth_token_raw.strip()
            auth_token = Auth.Token(auth_token_raw)
    g = Github(auth=auth_token)

    print(str(g.get_rate_limit()))
    try:
        target_repo = g.get_repo(target_repo_string)
    except Exception as e:
        print(f"Failed to reach repo due to the following exception \n {e}")
    
    target_commit_info_list = get_commit_info_list(target_repo)
    target_commit_info_num = len(target_commit_info_list)

    forked_repos_metadata_dict = dict()
    forked_repos_metadata_dict_reachable = dict()
    forked_repos_list = [forked_repo for forked_repo in target_repo.get_forks()]

    print(len(forked_repos_list))
    for forked_repo in forked_repos_list:
        forked_repo_name = forked_repo.full_name
        print(f"Querying {forked_repo_name} with {str(g.get_rate_limit())}")
        try:
            forked_commit_info_list = get_commit_info_list(forked_repo)
        except Exception as e:
            print(f"Failed to reach repo {forked_repo_name} due to the following exception \n {e}")
            forked_repos_metadata_dict[forked_repo_name] = dict()
            continue

        forked_commit_info_num = len(forked_commit_info_list)
        
        num_commits_diverged_target, num_commits_diverged_fork, last_common_commit = compare_target_forked_commits(target_commit_info_list, forked_commit_info_list)
        created_at_date = forked_repo.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        forked_repo_metadata = {
            "created_at": created_at_date,
            "num_commits_diverged_fork": num_commits_diverged_fork,
            "percent_commits_diverged_fork": round((num_commits_diverged_fork / forked_commit_info_num) * 100,2),
            "num_commits_diverged_target": num_commits_diverged_target,
            "percent_commits_diverged_target": round((num_commits_diverged_target / target_commit_info_num) * 100,2), 
            "last_common_commit": last_common_commit
        }
        forked_repos_metadata_dict[forked_repo_name] = forked_repo_metadata
        forked_repos_metadata_dict_reachable[forked_repo_name] = forked_repo_metadata

    # json_helper.save_json("./fork_examine.json", forked_repos_metadata_dict)
    forked_repos_metadata_df_reachable = pd.DataFrame(forked_repos_metadata_dict_reachable).T
    print(forked_repos_metadata_df_reachable)
    # forked_repos_metadata_df_reachable.to_csv(path_or_buf="./fork_examine.csv")
        
    
if __name__ == "__main__":
    main()