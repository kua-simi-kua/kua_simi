#!/bin/python 

import os
import hashlib
import json
import logging
from datetime import datetime

log = logging.getLogger()

# Set threshold of logger to info
log.setLevel(logging.INFO)

# Save file hashes to a JSON file
def save_to_json(nested_dict_repo_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    json_file_path = os.path.join("../repos_info/", f"repo_file_hashes_{timestamp}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(nested_dict_repo_name, json_file, indent=4)
    logging.info(f"Processing completed! File hashes saved to {json_file_path}.")

# File types of interest
file_types = (".py", ".sh")

# Directory containing repositories
repo_directory = "../repos/"

# Dictionary of repos and their respective files and hashes
def get_file_hash():
    # Loop through each subdirectory (repository) in /repos/
    nested_dict_repo_name = {}

    for repo_name in os.listdir(repo_directory):
        repo_path = os.path.join(repo_directory, repo_name)

        # Check if the path is a directory
        if os.path.isdir(repo_path):
            logging.info(f"'{repo_name}' is an onboarded code repository. Processing {repo_name}...\n")

            # Process files of interest and calculate hash
            file_hashes = {}
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file.endswith(file_types):
                        file_path = os.path.join(root, file)

                        # Calculate the hash
                        with open(file_path, "rb") as f:
                            file_content = f.read()
                            hash_value = hashlib.sha256(file_content).hexdigest()

                        # Print and store the hash as needed
                        logging.info(f"File: {file_path}, SHA256 Hash: {hash_value}")
                        file_hashes[file] = hash_value

            nested_dict_repo_name[repo_name] = file_hashes
            logging.info(f"Finished processing '{repo_name}'.\n")

    return nested_dict_repo_name

if __name__ == "__main__":
    nested_dict_repo_name = get_file_hash()
    save_to_json(nested_dict_repo_name)