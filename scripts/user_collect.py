from github import Github
from github import Auth
from argparse import ArgumentParser
from datetime import datetime
from utils import json_helper, constants, datetime_helper
import os


class UserWrapper:
    """
    A simple wrapper to handle pulling user data from GitHub.
    """
    def __init__(self, user_obj):
        self.user_obj = user_obj
        try:
            self.repos = user_obj.get_repos()
        except Exception as e:
            print(f"Error when get_repos() for {user_obj}")
            self.repos = []
    
    def get_starred_list(self):
        starred_list = []
        for page in self.user_obj.get_starred():
            try:
                starred_list.append(page.full_name)
            except Exception as e:
                print(f"Error occured for {page}: \n {e}")
                starred_list.append("Error")
        return starred_list, len(starred_list)
    
    def get_subscriptions_list(self):
        subscriptions_list = []
        for page in self.user_obj.get_subscriptions():
            try:
                subscriptions_list.append(page.full_name)
            except Exception as e:
                print(f"Error occured for {page}: \n {e}")
                subscriptions_list.append("Error")
        return subscriptions_list, len(subscriptions_list)
    
    def get_forked_owned_list(self):
        forked_list = []
        owned_list = []
        for page in self.repos:
            try:
                forked_list.append(page.full_name) if page.fork else owned_list.append(page.full_name)
            except Exception as e:
                print(f"Error occured for {page}: \n {e}")
                forked_list.append("Error")
                owned_list.append("Error")
        return forked_list, len(forked_list), owned_list, len(owned_list)
    
    def get_dict_repr(self):
        # forked_list, forked_count, owned_list, owned_count = self.get_forked_owned_list()
        # subscriptions_list, subscriptions_count = self.get_subscriptions_list()
        # starred_list, starred_count = self.get_starred_list()
        user_key_info_dict = {
            "location": self.user_obj.location,
            "twitter_username": self.user_obj.twitter_username,
            "created_at": datetime_helper.get_string_YYYYMMDD(self.user_obj.created_at),
            "updated_at": datetime_helper.get_string_YYYYMMDD(self.user_obj.updated_at),
            "followers": self.user_obj.followers,
            "following": self.user_obj.following,
            "public_gists_num": self.user_obj.public_gists,
            "public_repos_num": self.user_obj.public_repos,
            # "starred_list": starred_list,
            # "starred_count": starred_count,
            # "subscriptions_list": subscriptions_list,
            # "subscriptions_count": subscriptions_count,
            # "forked_list": forked_list,
            # "forked_count": forked_count,
            # "owned_list": owned_list,
            # "owned_count": owned_count
        }
        return user_key_info_dict

def main():
    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_string", help="repo_string to analyze.")
    argparser.add_argument("--token", "-t", help="Github token", nargs="?", default=None)
    argparser.add_argument("--date", "-d", help="Date of metadata to examine", default="latest")
    argparser.add_argument("--interact_type", "-it", nargs="*", default=constants.MOST_RELEVANT_INTERACT_TYPES)
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
    
    target_repo_dict = json_helper.read_json(metadata_full_filepath)

    user_list = []
    for interact_type in args.interact_type:
        user_list.extend(target_repo_dict[interact_type])
    user_list = list(set(user_list))
    user_total_num = len(user_list)    
    user_info_filepath = constants.USER_INFO_PATH + constants.USER_INFO_PREFIX + "1" + constants.JSON_SUFFIX

    user_counter = 0
    for user in user_list:
        user_counter += 1
        rate_limit = g.get_rate_limit()
        print(str(rate_limit))
        if not rate_limit.core.remaining:
            print(f"Rate limit is too low. Pls run again later (1 hour from {datetime_helper.get_string_YYYYMMDD_HHMMSS_UTC(datetime.now())})")
            break

        try:
            entry_created_at = datetime_helper.get_string_YYYYMMDD_HHMMSS_UTC(datetime.now())
            entry_updated_at = entry_created_at

            user_dict = json_helper.read_json(user_info_filepath)
            if not user_dict: 
                user_dict = {}
            elif user_dict.get(user):
                old_entry_created_at = user_dict[user]["entry_created_at"]
                old_entry_updated_at = user_dict[user]["entry_updated_at"]
                if datetime_helper.is_within_timedelta_hours(entry_updated_at, old_entry_updated_at, 2):
                    print(f"Not getting user {user_counter} / {user_total_num}: {user} since recently updated")
                    continue
                else:
                    entry_created_at = old_entry_created_at
            
            print(f"Getting user {user_counter} / {user_total_num} : {user}")
            user_obj = g.get_user(user)
            uw = UserWrapper(user_obj)
            user_key_info_dict = uw.get_dict_repr()
            user_key_info_dict["entry_created_at"] = entry_created_at
            user_key_info_dict["entry_updated_at"] = entry_updated_at

            user_dict[user] = user_key_info_dict
            json_helper.save_json(user_info_filepath, user_dict)
        except Exception as e:
            print(f"Error occurred for {user}: \n {e}")
            continue
    
    


if __name__ == "__main__":
    main()