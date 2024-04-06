from argparse import ArgumentParser
from utils import json_helper
import os

# metadata_pull also uses a similar function. May need to abstract out into utils/
def get_repo_string_from_url(repo_url):
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

# metadata_pull also uses a similar function. May need to abstract out into utils/
def obtain_repo_destination(repo_string):
    repo_string_token_list = repo_string.split("/")
    repo_destination = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    return repo_destination

def main():
    argparser = ArgumentParser(description="Clone given repos")
    argparser.add_argument("repo_config_file", help="Config file containing list of target repo URLs")
    args = argparser.parse_args()

    repo_list = json_helper.read_json(args.repo_config_file)
    print("Taking in list of target repos from config file ", args.repo_config_file)

    for target_repo_url in repo_list:
        print(f"Start cloning {target_repo_url}")
        destination_repo = f"../repos/{obtain_repo_destination(get_repo_string_from_url(target_repo_url))}"
        os.system(f"git clone {target_repo_url} {destination_repo}")
        print(f"Finish cloning {target_repo_url} into {destination_repo}")


if __name__ == "__main__":
    main()