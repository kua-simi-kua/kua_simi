from datetime import datetime
from argparse import ArgumentParser
from utils import json_helper
import os

REPOS_INFO_PATH = "../repos_info/auth_metadata/"
JSON_EXT = ".json"

def main():
    argparser = ArgumentParser(description="slice all the repo_info huge json into small per day files")
    argparser.add_argument("repos_info_name")
    args = argparser.parse_args()

    repos_info_name = args.repos_info_name
    big_json_path = REPOS_INFO_PATH + repos_info_name + JSON_EXT
    metadata_dict = json_helper.read_json(big_json_path)

    new_dir_path = REPOS_INFO_PATH + repos_info_name + "/"
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    new_file_path_root = new_dir_path + repos_info_name + "___"

    for timestamp in metadata_dict.keys():
        float_timestamp = float(timestamp) / 1e3
        date_of_timestamp = datetime.fromtimestamp(float_timestamp).strftime("%Y%m%d")
        new_file_pathname = new_file_path_root + date_of_timestamp + JSON_EXT
        
        new_file_data = metadata_dict[timestamp]
        json_helper.save_json(new_file_pathname, new_file_data)
        print(new_file_pathname)
        

    # epoch_time = "1724639232315"
    # epoch_time = float(epoch_time) / 1e3
    # date_time = datetime.fromtimestamp(epoch_time)

    # # Format the datetime object to a date string
    # date_string = date_time.strftime("%Y%m%d")
    # print(date_string)


if __name__ == "__main__":
    main()