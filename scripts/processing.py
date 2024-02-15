#!/bin/python 

import os
import hashlib
import json

# Save file hashes to a JSON file
def save_to_json(nested_dict_repo_name):
    json_file = os.path.join("../repos_info/", "repo_file_hashes.json")
    with open(json_file, 'w') as json_file:
        json.dump(nested_dict_repo_name, json_file, indent=4)
    print(f"File hashes saved to {json_file}.")

# File types of interest
file_types = (".py", ".sh")
# Dictionary of repos and their respective files and hashes
def get_file_hash():
    # Loop through each subdirectory (repository) in /repos/
    nested_dict_repo_name = {}
    for repo_name in os.listdir(repo_directory):
        repo_path = os.path.join(repo_directory, repo_name)
        # Check if the path is a directory
        try:
            if os.path.isdir(repo_path):
                print(f"Processing {repo_name}...\n")
        except:
            print(f"Processing {repo_name} failed.")
        # Process files of interests and calculate hash
        for root, dirs, files in os.walk(repo_directory):
            file_hashes = {}
            for file in files:
                if file.endswith(file_types):
                    file_path = os.path.join(root, file)
                    print(file_path)
                    # Calculate the hash
                    with open(file_path, "rb") as f:
                        file_content = f.read()
                        hash_value = hashlib.sha256(file_content).hexdigest()
                        # Print and store the hash as needed
                        print(f"File: {file_path}, SHA256 Hash: {hash_value}")
                        file_hashes[file] = hash_value
        nested_dict_repo_name[repo_name] = file_hashes
        print(f"\nFinished processing {repo_name}.")
    return nested_dict_repo_name

if __name__ == "__main__":
    # Directory containing repositories
    repo_directory = "../repos/"

    nested_dict_repo_name = get_file_hash()
    save_to_json(nested_dict_repo_name)