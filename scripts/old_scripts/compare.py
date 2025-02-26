#!/bin/python 

import json
import os
import logging
import re
from datetime import datetime

log = logging.getLogger()

# Set threshold of logger to info
log.setLevel(logging.INFO)

def enumerate_json_files(directory_path):
    json_files = []
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file has a .json extension
        if filename.endswith(".json"):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)
            json_files.append(file_path)
    return json_files


# Directory containing cloned repositories
repo_directory = "../repos/"

def file_age(file1_path, file2_path):    
    pattern = r"\d+"

    # Use re.search to find the first match in the filename
    match1 = re.search(pattern, file1_path)
    match2 = re.search(pattern, file2_path)

    if int(match2.group()) > int(match1.group()):
        old_file = file1_path
        new_file = file2_path
    else:
        old_file = file2_path
        new_file = file1_path

    logging.info(f"\nOlder file '{old_file}'.\nNewer file '{new_file}'.")
    return new_file, old_file

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def compare_and_append_changes(new_data, old_data):
    # Loop through first level of new json data --- repo
    for new_repo, new_repo_data in new_data.items():
        # Check if the new repos of the new json exist in the old json
        logging.info(f"Repos in old_file: {list(old_data.keys())}")       
        if new_repo not in list(old_data.keys()):
            logging.info(f"The repo {new_repo} is not found in the old json: {old_data}")
            # Add the repo's data to old json if it doesn't exist
            old_data[new_repo] = new_data[new_repo]
            logging.info(f"{old_data[new_repo]}")
            save_json(old_file, old_data)
            logging.info(f"Old json file updated with {new_repo}")
            continue
        # Loop through second level of new json data --- files
        for new_file, new_file_data_list in new_repo_data.items():
            for new_file_data in new_file_data_list:
                new_hash = new_file_data["sha256"]
                new_hash_first_seen = new_file_data["first_seen"]
                new_hash_last_seen = new_file_data["last_seen"]
                logging.info(f"New hash: {new_hash}, First Seen Timestamp: {new_hash_first_seen}")
                
                # Check if the file exists in old_data
                if new_file in old_data[new_repo]:
                    logging.info(f"New file {new_file} exists in old json.")
                    old_hashes = [item["sha256"] for item in old_data[new_repo][new_file]]
                    logging.info(f"Old hash list: {old_hashes}")
                    # Check if the new hash is not in old hashes
                    if new_hash not in old_hashes:
                        logging.info(f"New hash {new_hash} not in {old_hashes}")
                        # Append changes to the old data
                        old_data[new_repo][new_file].append({
                            "sha256": new_hash,
                            "first_seen": new_hash_first_seen,
                            "last_seen": new_hash_last_seen
                        })
                        logging.info(f"Appended {new_hash} into '{new_file}' of '{new_repo}' in old json.")
                        save_json(old_file, old_data)
                    # If new hash exists in old hashes, update last_seen timestamp
                    else:
                        logging.info(f"Hash for '{new_file}' in '{new_repo}' already exists.")
                        for i in old_data[new_repo][new_file]:
                            if i["sha256"] == new_hash:
                                i["last_seen"] = new_hash_last_seen
                                logging.info(f"Updating last_seen timestamp for '{new_file}' in old_data")
                                save_json(old_file, old_data)
                else:
                    # Add the file's data to old json if it doesn't exist
                    old_data[new_repo][new_file] = [{
                        "sha256": new_hash,
                        "first_seen": new_hash_first_seen,
                        "last_seen": new_hash_last_seen
                    }]
                    logging.info(f"Added new file '{new_file}' in '{new_repo}' to old json.")
                    save_json(old_file, old_data)

def delete_json_file(file_path):
    try:
        os.remove(file_path)
        logging.info(f"Older file '{file_path}' deleted successfully.")
    except FileNotFoundError:
        logging.info(f"File '{file_path}' not found.")
    except Exception as e:
        logging.info(f"An error occurred while deleting the file: {e}")

if __name__ == "__main__":
    # Enumerate json files in repos_info
    directory_path = "../repos_info/"
    json_files = enumerate_json_files(directory_path)
    if json_files:
        logging.info("Found JSON files:")
        for json_file in json_files:
            logging.info(json_file)
    else:
        logging.info("No JSON files found in the specified directory.")

    # Compare json files in repos_info
    file1_path = json_files[0]
    file2_path = json_files[1]
    new_file, old_file = file_age(file1_path, file2_path)
    new_data = load_json(new_file)
    old_data = load_json(old_file)
    if new_data == old_data:
        # delete_json_file(old_file)
        logging.info("Both files have the same data, deleting older json file.")
    else:
        compare_and_append_changes(new_data, old_data)
        # delete_json_file(new_file)