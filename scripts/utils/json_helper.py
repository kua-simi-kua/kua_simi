import json
import os
import logging

# Returns None if filename doesn't exist (silent fail)
def read_json(json_file_path): 
    repo_data_obj = None
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            repo_data_obj = json.load(json_file)
    return repo_data_obj