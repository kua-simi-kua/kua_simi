from github import Github
from github import Auth
from github import GithubIntegration
from argparse import ArgumentParser
from datetime import datetime

from utils import json_helper

import json
import os
import logging


REPOS_INFO_PATH = "../repos_info/auth_metadata/"
GITHUB_METADATA_JSON_PREFIX = "github_metadata___"

def get_repo_string_from_url(repo_url):
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    print(repo_string)
    return repo_string

def obtain_collected_metadata_filepath(repo_string):
    repo_string_token_list = repo_string.split("/")
    metadata_filename = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    full_file_path = os.path.join(REPOS_INFO_PATH, f"{GITHUB_METADATA_JSON_PREFIX}{metadata_filename}.json")
    return full_file_path

def main():
    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_config_file", help="Config file containing list of target repo URLs")
    args = argparser.parse_args()

    # Authentication
    with open("../config/github_auth_super.pass", "r") as pass_file: # ensure that this file is not committed/pushed
        auth_token = pass_file.read()
        auth_token.strip()
    g = Github(auth_token)
    print(g.get_rate_limit())

    repo_list = json_helper.read_json(args.repo_config_file)
    print("Taking in list of target repos from config file ", args.repo_config_file)

    for target_repo_url in repo_list:
        # parse through target repo url and GET the repo object 
        print(f"Start pulling metadata for {target_repo_url}")
        target_repo_string = get_repo_string_from_url(target_repo_url)
        target_repo = g.get_repo(target_repo_string)

        # Prep relevant metadata
        watcher_list = []
        for page in target_repo.get_watchers():
            watcher_list.append(page.login)

        stargazer_list = []
        for page in target_repo.get_stargazers():
            stargazer_list.append(page.login)

        contributor_list = []
        for page in target_repo.get_contributors():
            contributor_list.append(page.login)
        contributor_count = len(contributor_list)

        open_pull_request_list = []
        for page in target_repo.get_pulls():
            open_pull_request_list.append(page.title)
        open_pull_request_count = len(open_pull_request_list)

        labels_list = []
        for page in target_repo.get_labels():
            labels_list.append(page.name)
        labels_count = len(labels_list)

        forkers_list = []
        for page in target_repo.get_forks():
            forkers_list.append(page.owner.login)

        subscribers_list = []
        for page in target_repo.get_subscribers():
            subscribers_list.append(page.login)
        
        committers_list = []
        for page in target_repo.get_commits():
            committers_list.append(page.author.login)
        committers_count = len(set(committers_list))

        committers_email_list = []
        for page in target_repo.get_commits():
            committers_email_list.append(page.commit.author.email)
        committers_email_count = len(set(committers_email_list))

        assignees_list = []
        for page in target_repo.get_assignees():
            assignees_list.append(page.login)
        assignees_count = len(assignees_list)

        # Prep metadata_filepath to store updated info
        # if metadata_filepath does not exist, creat empty dict to store info
        metadata_filepath = obtain_collected_metadata_filepath(target_repo_string)
        metadata_dict = json_helper.read_json(metadata_filepath)
        if not metadata_dict:
            metadata_dict = {}

        # Collect metadata of the target repo at specified timestamp
        # then append it to the current json file for that target repo

        timestamp = int(datetime.now().timestamp() * 1000)
        metadata_at_timestamp_dict = {
            "forks_count": target_repo.forks_count,
            "forkers": forkers_list,
            "stargazers_count": target_repo.stargazers_count,
            "stargazers": stargazer_list,
            "watchers_count": target_repo.watchers_count,
            "watchers": watcher_list,
            "contributor_count": contributor_count,
            "contributors": contributor_list,
            "open_pull_request_count": open_pull_request_count,
            "open_pull_requests": open_pull_request_list,
            "label_count": labels_count,
            "labels": labels_list,
            "subscribers": subscribers_list,
            "subscribers_count": target_repo.subscribers_count,
            "committers": committers_list,
            "committers_count": committers_count,
            "committers_emails": committers_email_list,
            "committers_emails_count": committers_email_count,
            "assignees": assignees_list,
            "assignees_count": assignees_count
        }
        metadata_dict[timestamp] = metadata_at_timestamp_dict
        print(metadata_at_timestamp_dict)

        json_helper.save_json(metadata_filepath, metadata_dict)
        print(f"\nFinish pulling metadata for {target_repo_url}")

    
if __name__ == "__main__":
    main()