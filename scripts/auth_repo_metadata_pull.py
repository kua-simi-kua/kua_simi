from github import Github
from github import Auth
from github import GithubIntegration
from argparse import ArgumentParser
from datetime import datetime, date
import time
import os
from utils import json_helper, constants, SpaceLaunchPad

# class RepoProxy:

#     def __init__(self, github_obj, repo_string):
#         self.repository = github_obj.get_repo(repo_string)

#     def get_contributors_list(self):
#         return [contributor for contributor in self.repository.get_contributors()]
    
#     def get_stargazers_list(self):
#         return [stargazer for stargazer in self.repository.get_stargazers()]

def get_repo_string_from_url(repo_url):
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

def obtain_collected_metadata_filepath(repo_string):
    repo_string_token_list = repo_string.split("/")
    metadata_string = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    repos_info_folder_path = constants.REPOS_INFO_METADATA_PATH + f"{metadata_string}/"

    today_date = date.today().strftime("%Y%m%d")
    metadata_filename = metadata_string + "___" + today_date
    full_file_path = os.path.join(repos_info_folder_path, f"{metadata_filename}.json")

    do_key = f"repos_info/auth_metadata/{metadata_string}/{metadata_filename}.json"
    return do_key, full_file_path    


def main():
    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_config_file", help="Config file containing list of target repo URLs")
    argparser.add_argument("--token", "-t", help="Github token", nargs="?", default=None)
    argparser.add_argument("--do_token", "-dt", help="DigitalOcean Key ID and Key Secret", nargs=2, default=None)
    args = argparser.parse_args()

    if args.token:
        auth_token = Auth.Token(args.token)
    else:
        with open("../config/github_auth_super.pass", "r") as pass_file: # ensure that this file is not committed/pushed
            auth_token_raw = pass_file.read()
            auth_token_raw.strip()
            auth_token = Auth.Token(auth_token_raw)
    g = Github(auth=auth_token)

    do_token_list = args.do_token
    space_launch_pad = SpaceLaunchPad.SpaceLaunchPad(do_token_list[0], do_token_list[1])

    repo_list = json_helper.read_json(args.repo_config_file)
    print(f"Taking in list of target repos from config file {args.repo_config_file}")

    for target_repo_url in repo_list:
        rate_limit_msg = str(g.get_rate_limit())
        print(rate_limit_msg)
        # parse through target repo url and GET the repo object 
        start_time = time.perf_counter()
        print(f"Start pulling metadata for {target_repo_url}")
        target_repo_string = get_repo_string_from_url(target_repo_url)
        try:
            target_repo = g.get_repo(target_repo_string)
        except Exception as e:
            print(f"Failed to reach repo due to the following exception \n {e}")

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
        authors_list = []
        for page in target_repo.get_commits():
            try:
                committer_login = page.committer.login
            except Exception as e:
                print(f"Unable to get committer login from {page} due to error {e}")
            else:
                committers_list.append(committer_login)
            
            try:
                author_login = page.author.login
            except Exception as e:
                print(f"Unable to get author login from {page} due to error {e}")
            else:
                authors_list.append(author_login)
        committers_count = len(set(committers_list))
        authors_count = len(set(authors_list))

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
        do_key, metadata_filepath = obtain_collected_metadata_filepath(target_repo_string)

        # append metadata to the current json file for that target repo
        metadata_dict = {
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
            "authors": authors_list,
            "authors_count": authors_count,
            "assignees": assignees_list,
            "assignees_count": assignees_count
        }
        # print(metadata_at_timestamp_dict)

        json_helper.save_json(metadata_filepath, metadata_dict)

        space_launch_pad.launch_to_space(key=do_key, file_path=metadata_filepath)
        print(f"Finish pulling metadata for {target_repo_url}")
        end_time = time.perf_counter()
        time_elapsed = round(end_time - start_time, 2)
        print(f"{time_elapsed}s elapsed")


    
if __name__ == "__main__":
    main()