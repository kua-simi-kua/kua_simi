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



def main():
    argparser = ArgumentParser(description="Pull GitHub metadata of a given list of users")
    argparser.add_argument("repo_metadata_file", help="File containing repo metadata")
    args = argparser.parse_args()

    # Authentication
    with open("../config/github_auth_super.pass", "r") as pass_file: # ensure that this file is not committed/pushed
        auth_token = pass_file.read()
        auth_token.strip()
    g = Github(auth_token)
    print(g.get_rate_limit())

    repo_metadata_obj = json_helper.read_json(args.repo_metadata_file)
    print("Taking in repo metadata from", args.repo_metadata_file)

    # the int() and str() conversions because json keys cannot be int
    timestamp_list = [int(timestamp_key) for timestamp_key in repo_metadata_obj.keys()]
    timestamp_list.sort()
    most_recent_timestamp = timestamp_list.pop()
    most_recent_metadata = repo_metadata_obj[str(most_recent_timestamp)]

    watcher_list = most_recent_metadata["watchers"]
    print("watcher_list: ", watcher_list)

    contributor_list = most_recent_metadata["contributors"]
    print("contributor_list: ", contributor_list)

    user_list = list(set(watcher_list + contributor_list))
    user_list_dict = {}
    for user in user_list:
        print("Getting ", user)
        user_obj = g.get_user(user)
        user_info = {
            "watched": user_obj.get_watched(),
            "starred": user_obj.get_starred()
        }
        user_list_dict[user] = user_info
    print("user_list_dict: ", user_list_dict)

    # Not implemented yet
    # stargazer_list = most_recent_metadata["stargazers"]
    # print("stargazer_list: ", stargazer_list)

    


    
if __name__ == "__main__":
    main()