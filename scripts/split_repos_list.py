from argparse import ArgumentParser
from utils import json_helper

def main():
    argparser = ArgumentParser(description="Split the long repos_list.json into smaller json")
    argparser.add_argument("long_repo_config_file", help="Config file containing list of target repo URLs")
    argparser.add_argument("-n", "--num", help="Number of repo urls in each smaller repo_list json files", nargs="?", default=5, const=5)
    args = argparser.parse_args()

    long_repo_config_file = args.long_repo_config_file
    num = args.num
    print(f"Splitting {long_repo_config_file} into small lists of {num}")

    long_repo_list = json_helper.read_json(long_repo_config_file)
    list_of_lists = [long_repo_list[i * num:(i + 1) * num] for i in range((len(long_repo_list) + num - 1) // num)]
    
    for index in range(len(list_of_lists)):
        small_repos_list_name = f"../config/repos_list_dir/repos_list_{index}.json"
        json_helper.save_json(small_repos_list_name, list_of_lists[index])
        print(f"Created smaller repos list in {small_repos_list_name}")




if __name__ == "__main__":
    main()