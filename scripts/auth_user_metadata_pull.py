from github import Github
from github import Auth
from github import GithubIntegration
from argparse import ArgumentParser
from datetime import datetime

from utils import json_helper

class UserWrapper:
    """
    A simple wrapper around the raw user object retrieved from GitHub.
    """
    def __init__(self, user_obj):
        self.user_obj = user_obj
        self.watched = self.query_watched()
        self.starred = self.query_starred()
        self.repos = self.query_repos()
    
    def query_watched(self):
        watched_list = []
        for page in self.user_obj.get_watched():
            watched_list.append(page.full_name)
        return watched_list
    
    def query_starred(self):
        starred_list = []
        for page in self.user_obj.get_starred():
            starred_list.append(page.full_name)
        return starred_list
    
    def query_repos(self):
        repos_list = []
        for page in self.user_obj.get_repos():
            repos_list.append(page.full_name)
        return repos_list 
    
    def get_watched(self):
        return self.watched

    def get_watched_count(self): 
        return len(self.watched)
    
    def get_starred(self):
        return self.starred

    def get_starred_count(self):
        return len(self.starred)

    def get_repos(self):
        return self.repos
    
    def get_repos_count(self):
        return len(self.repos)


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
    contributor_list = most_recent_metadata["contributors"]
    stargazer_list = most_recent_metadata["stargazers"]

    user_list = list(set(watcher_list + contributor_list + stargazer_list))
    user_list_dict = {}
    for username in user_list:
        print(g.get_rate_limit())
        print("Getting ", username)
        user_obj = g.get_user(username)
        user_obj_wrapper = UserWrapper(user_obj)

        watched_list = []
        for repo_obj in user_obj.get_watched():
            watched_list.append(repo_obj.full_name)

        user_info = {
            "watched": user_obj_wrapper.get_watched,
            "starred": user_obj_wrapper.get_starred(),
            "repos": user_obj_wrapper.get_repos()
        }
        user_list_dict[username] = user_info
    print("user_list_dict: ", user_list_dict)
 


    
if __name__ == "__main__":
    main()