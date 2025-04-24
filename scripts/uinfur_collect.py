from github import Github
from github import Auth
from argparse import ArgumentParser
from datetime import datetime, date
from utils import json_helper, constants
import os


def main():
    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_string", help="repo_string to analyze.")
    argparser.add_argument("--token", "-t", help="Github token", nargs="?", default=None)
    argparser.add_argument("--date", "-d", help="Date of metadata to examine", default="latest")
    args = argparser.parse_args()

    if args.token:
        auth_token = Auth.Token(args.token)
    else:
        with open("../config/github_auth_super.pass", "r") as pass_file: # ensure that this file is not committed/pushed
            auth_token_raw = pass_file.read()
            auth_token_raw.strip()
            auth_token = Auth.Token(auth_token_raw)
    g = Github(auth=auth_token)

    metadata_repo_dir_path = constants.REPOS_INFO_METADATA_PATH + args.repo_string + '/'
    if args.date == "latest": 
        metadata_files_list = sorted(os.listdir(metadata_repo_dir_path))
        metadata_full_filepath = metadata_repo_dir_path + metadata_files_list[-1]
    else:
        metadata_full_filepath = metadata_repo_dir_path + args.repo_string + args.date + constants.JSON_SUFFIX
    
    print(metadata_full_filepath)
    target_repo_dict = json_helper.read_json(metadata_full_filepath)

    user_dict = {}
    target_repo_stargazers = target_repo_dict.get("stargazers")
    for stargazer in target_repo_stargazers:
        print(str(g.get_rate_limit()))
        user_obj = g.get_user(stargazer)
        user_key_info = {
            "location": user_obj.location,
            "twitter_username": user_obj.twitter_username,
            "created_at": user_obj.created_at,
            "updated_at": user_obj.updated_at,
            "followers": user_obj.followers,
            "following": user_obj.following,
            "public_gists": user_obj.public_gists,
            "public_repos": user_obj.public_repos
        }
        user_dict[user_obj.login] = user_key_info        

    


if __name__ == "__main__":
    main()