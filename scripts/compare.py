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
    # Loop through first level of new json data
    for new_repo, new_repo_data in new_data.items():
        # Loop through second level of new json data
        for new_file, new_file_data in new_repo_data.items():
            new_hash = new_file_data['sha256']
            logging.info(f"New hash: {new_hash}.")
            new_date = new_file_data['hash_timestamp']
            logging.info(f"New hash timestamp: {new_date}.")
            # Check if the file exists in old_data
            if new_file in old_data[new_repo]:
                logging.info(f"New file {new_file} exists in old json {old_data[new_repo]}.")
                old_hashes = old_data[new_repo][new_file]['sha256']
                logging.info(f"Old hash list: {old_hashes}")
                # Check if the new hash is not in old hashes
                if new_hash[0] not in old_hashes:
                    logging.info(f"New hash {new_hash} not in {old_hashes}")
                    # Append changes to the old data
                    old_data[new_repo][new_file]['sha256'].extend(new_hash)
                    old_data[new_repo][new_file]['hash_timestamp'].extend(new_date)
                    logging.info(f"Appended {new_hash} into '{new_file}' of '{new_repo}' of {old_data}.")
                    save_json(old_file, old_data)
                else:
                    logging.info(f"Hash for '{new_file}' in '{new_repo}' of {old_data} already exists.")
            else:
                # Add the file to old data if it doesn't exist
                old_data[new_repo][new_file] = {'sha256': [new_hash], 'hash_timestamp': [new_date]}
                logging.info(f"Added new file '{new_file}' in '{new_repo}' of '{old_data}'.")
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
        delete_json_file(old_file)
        logging.info("Both files have the same data, deleting older json file.")
    else:
        compare_and_append_changes(new_data, old_data)
        delete_json_file(new_file)