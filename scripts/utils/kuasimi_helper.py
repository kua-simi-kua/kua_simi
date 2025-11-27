from utils import json_helper

CONFIG_ALL_REPOS_PATH = "../config/repos_list_long.json"

def get_repo_slash_string_from_url(repo_url):
    """
    Given a repo URL https://github.com/USER/REPO , return the repo slash string USER/REPO .
    This is needed for the Github object to query the API for the repo.
    """
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

def get_repo_string_from_slash_string(repo_slash_string):
    """
    Given a repo slash string USER/REPO, return the repo string USER___REPO.
    """
    repo_string_token_list = repo_slash_string.split("/")
    repo_string = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    return repo_string

def get_all_repo_strings():
    """
    Return all repos currently tracked in repos_list_long.json.
    """
    all_repos_list = json_helper.read_json(CONFIG_ALL_REPOS_PATH)
    all_repo_strings_list = [get_repo_string_from_slash_string(
        get_repo_slash_string_from_url(repo_url)
        ) for repo_url in all_repos_list]
    return all_repo_strings_list