#!/bin/python 

import os
import hashlib

# file types of interests
file_types = (".py", ".sh")

# Specify the directory containing repositories
repo_directory = "~/repos/"

# Loop through each subdirectory (repository) in /repos/
for repo_name in os.listdir(repo_directory):
    repo_path = os.path.join(repo_directory, repo_name)

    # Check if the path is a directory and contains a .git subdirectory
    if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
        print(f"Processing {repo_name}...")

    # Process .py files and calculate hash
    for root, dirs, files in os.walk(repo_directory):
        for file in files:
            if file.endswith(file_types):
                file_path = os.path.join(root, file)

                # Calculate the hash (MD5 in this example)
                with open(file_path, "rb") as f:
                    file_content = f.read()
                    hash_value = hashlib.sha256(file_content).hexdigest()

                # Print or store the hash as needed
                print(f"File: {file_path}, SHA256 Hash: {hash_value}")
    
    print(f"Finished processing {repo_name}.")