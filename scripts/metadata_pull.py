from github import Github
from argparse import ArgumentParser
from datetime import datetime

import json
import os
import logging

REPOS_INFO_PATH = "../repos_info/"

def get_repo_string_from_url(repo_url):
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

def obtain_collected_metadata_filename(repo_string):
    repo_string_token_list = repo_string.split("/")
    metadata_filename = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    return metadata_filename

# returns empty dict if file doesn't exist
def read_from_json(repo_string): # abstract this out into utilities
    filename_repo_suffix = obtain_collected_metadata_filename(repo_string)
    json_file_path = os.path.join(REPOS_INFO_PATH, f"github_metadata_{filename_repo_suffix}.json")
    repo_data_obj = {}
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            repo_data_obj = json.load(json_file)
    return repo_data_obj

# TODO: save the dictionary into a list of dictionaries / json file 
def save_to_json(repo_string, data_obj): # abstract this out into utilities
    filename_repo_suffix = obtain_collected_metadata_filename(repo_string)
    json_file_path = os.path.join(REPOS_INFO_PATH, f"github_metadata_{filename_repo_suffix}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(data_obj, json_file, indent=4)
    logging.info(f"Processing completed! File hashes saved to {json_file_path}.")

def main():
    # starList = repo.get_stargazers_with_dates()
    # print("starList; ")
    # for starPage in starList:
    #     print(starPage)

    # forkList = repo.get_forks()
    # print("forkList: ")
    # for forkPage in forkList:
    #     print(forkPage)

    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_url", help="GitHub URL of the repo")

    args = argparser.parse_args()
    repo_string = get_repo_string_from_url(args.repo_url)

    g = Github()
    print("rate_limit: ", g.get_rate_limit())
    repo = g.get_repo(repo_string)

    metadata_dict = read_from_json(repo_string)
    print("initial metadata_dict: ", metadata_dict)

    timestamp = int(datetime.now().timestamp() * 1000)
    metadata_at_timestamp_dict = {
        "forks_count": repo.forks_count,
        "stars_count": repo.stargazers_count
    }

    metadata_dict[timestamp] = metadata_at_timestamp_dict
    print("end metadata_dict: ", metadata_dict)

    save_to_json(repo_string, metadata_dict)
    

    
if __name__ == "__main__":
    main()