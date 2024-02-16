#!/bin/python 

import json
import os
import logging
import re

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

def determine_newer_json(file1_path, file2_path):    
    # Extract the datetime string portion
    # Define a regular expression pattern to match the number portion
    pattern = r"\d+"

    # Use re.search to find the first match in the filename
    match1 = re.search(pattern, file1_path)
    if match1:
        number_portion1 = match1.group()
        logging.info(f"File 1 is {number_portion1}")

    match2 = re.search(pattern, file2_path)
    if match2:
        number_portion2 = match2.group()
        logging.info(f"File 2 is {number_portion2}")

    try:
        int1 = int(number_portion1)
        int2 = int(number_portion2)

        if int1 > int2:
            logging.info(f"'{file1_path}' is the newer file")
            newer_file = file1_path
            older_file = file2_path
        else:
            logging.info(f"'{file2_path}' is the newer file")
            newer_file = file2_path
            older_file = file1_path
        return newer_file, older_file

    except ValueError:
        logging.info("Both json files are of the same age.")

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def compare_and_append_changes(old_data, new_data):
    for key, new_values in new_data.items():
        if key in old_data:
            old_values = old_data[key]
            for subkey, new_value in new_values.items():
                if subkey not in old_values or old_values[subkey] != new_value:
                    old_values[subkey] = new_value
                    old_values[f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"] = new_value
        else:
            old_data[key] = new_values

def delete_older_json_file(file_path):
    try:
        os.remove(older_json_file)
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
    newer_json_file = determine_newer_json(file1_path, file2_path)
    delete_older_json_file(older_json_file)