from github import Github
from github import Auth
from argparse import ArgumentParser
from datetime import datetime, date
import time
import os

class RepoProxy:

    def __init__(self, github_obj, repo_string):
        self.repository = github_obj.get_repo(repo_string)

    def get_contributors_list(self):
        return [contributor for contributor in self.repository.get_contributors()]
    
    def get_stargazers_list(self):
        return [stargazer for stargazer in self.repository.get_stargazers()]


def main():
    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_string", help="repo_string")
    argparser.add_argument("--token", "-t", help="Github token", nargs="?", default=None)
    args = argparser.parse_args()

    if args.token:
        auth_token = Auth.Token(args.token)
    else:
        with open("../config/github_auth_super.pass", "r") as pass_file: # ensure that this file is not committed/pushed
            auth_token_raw = pass_file.read()
            auth_token_raw.strip()
            auth_token = Auth.Token(auth_token_raw)
    g = Github(auth=auth_token)

    target_repo_proxy = RepoProxy(g, args.repo_string)
    target_repo_stargazers = target_repo_proxy.get_stargazers_list()
    count = 0
    for stargazer in target_repo_stargazers:
        count += 1
        if count > 10: break
        print(str(g.get_rate_limit()))
        print((
            stargazer.login,
            stargazer.location,
            stargazer.twitter_username,
            stargazer.created_at,
            stargazer.updated_at,
            stargazer.followers,
            stargazer.following,
            stargazer.public_gists,
            stargazer.public_repos
        ))
    # target_repo_stargazer_with_stats = [
    #     (
    #         stargazer.followers,
    #         stargazer.following,
    #         stargazer.public_gists,
    #         stargazer.public_repos,
    #         stargazer.role,
    #         stargazer.starred_at
    #     )
    #         for stargazer in target_repo_stargazers
    # ]
    # print(target_repo_stargazer_with_stats)

    


if __name__ == "__main__":
    main()