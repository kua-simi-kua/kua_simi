from github import Github
from github import Auth
from github import GithubIntegration
from argparse import ArgumentParser
from datetime import datetime

from utils import json_helper

import json
import os
import logging
import base64


REPOS_INFO_PATH = "../repos_info/auth_metadata/"

def get_repo_string_from_url(repo_url):
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

def obtain_collected_readme_filepath(repo_string):
    repo_string_token_list = repo_string.split("/")
    readme_filename = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    full_file_path = os.path.join(REPOS_INFO_PATH, f"{readme_filename}___readme.txt")
    return full_file_path

def main():
    argparser = ArgumentParser(description="Pull readme of a given repo")
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

    readme_failures = []

    for target_repo_url in repo_list:
        # parse through target repo url and GET the repo object 
        print(f"Start pulling readme for {target_repo_url}")
        target_repo_string = get_repo_string_from_url(target_repo_url)
        target_repo = g.get_repo(target_repo_string)
        readme_filepath = obtain_collected_readme_filepath(target_repo_string)

        # readme querying. may fail when querying or when writing into file
        try:
            content_obj = target_repo.get_readme()
            readme_base64 = content_obj.content
            readme = base64.b64decode(readme_base64).decode("utf-8",errors="ignore")
        
            with open(readme_filepath, "w") as file_obj:
                file_obj.write(readme)
        except Exception as e:
            print("Encountered error:")
            print(e)
            print(f"Please manually download the README at {target_repo_url}")
            readme_failures.append((target_repo_url,readme_filepath))
        
    if len(readme_failures):
        print("Please manually download the READMEs for the target repos into the following files: ")
        for failure in readme_failures:
            print(failure)




    
if __name__ == "__main__":
    main()