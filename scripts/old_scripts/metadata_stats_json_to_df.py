from utils import json_helper
import json
import os
import pandas as pd
import logging

log = logging.getLogger()

# Set threshold of logger to info
log.setLevel(logging.INFO)

REPOS_INFO_PATH = "../repos_info/auth_metadata/"
GITHUB_METADATA_STATS_JSON_PREFIX = "github_metadata_stats___"

# Function to retrieve a list of metadata_stats_json_files
def enumerate_metadata_stats_json_files(directory_path):
    metadata_stats_json_files = []
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is one of the metadata files of interest
        if filename.startswith(f"{GITHUB_METADATA_STATS_JSON_PREFIX}"):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)
            metadata_stats_json_files.append(file_path)
    if metadata_stats_json_files:
        metadata_json_files_count = len(metadata_stats_json_files)
        logging.info(f"Found {metadata_json_files_count} Github metadata stats json files")
        for metadata_stats_json_file in metadata_stats_json_files:
            logging.info(metadata_stats_json_file)
    else:
        logging.info("No Github metadata json file found in the specified directory.")
    return metadata_stats_json_files

# Function to retrieve a the full path and filename of the json file of interest
def obtain_collected_metadata_stats_filepath(metadata_stats_json_file):
    delimiters = ["_", "___", ".", "/", "\\"]
    for delimiter in delimiters:
        metadata_stats_json_file = " ".join(metadata_stats_json_file.split(delimiter))
    metadata_stats_json_file_token_list = metadata_stats_json_file.split()
    metadata_stats_filename = metadata_stats_json_file_token_list[-3] + "__" + metadata_stats_json_file_token_list[-2]
    metadata_stats_full_file_path = os.path.join(REPOS_INFO_PATH, f"{GITHUB_METADATA_STATS_JSON_PREFIX}{metadata_stats_filename}.json")
    logging.info(metadata_stats_filename)
    logging.info(metadata_stats_full_file_path)
    return metadata_stats_full_file_path, metadata_stats_filename

# Function to convert nested JSON string to DataFrame
def convert_nested_json_to_dataframe(json_data, metadata_stats_filename):
    df_dict = {}
    for key, nested_json_str in json_data[str(metadata_stats_filename)].items():
        nested_dict = json.loads(nested_json_str)
        if isinstance(nested_dict, dict):
            df = pd.DataFrame.from_dict(nested_dict, orient='index')
        else:
            df = pd.DataFrame(nested_dict)
        df_dict[key] = df
    return df_dict

# Convert and print DataFrames
def main():

    # Enumerate github metadata json files in ../repos_info/auth_metadata
    directory_path = "../repos_info/auth_metadata"

    metadata_stats_json_files = enumerate_metadata_stats_json_files(directory_path)
    for metadata_stats_json_file in metadata_stats_json_files:

        metadata_dict = json_helper.read_json(metadata_stats_json_file)
        metadata_stats_full_file_path, metadata_stats_filename = obtain_collected_metadata_stats_filepath(metadata_stats_json_file)
        dfs = convert_nested_json_to_dataframe(metadata_dict, metadata_stats_filename)

        for key, df in dfs.items():
            logging.info(f"DataFrame for {key}:")
            logging.info(df)
            # logging.info("\n")

if __name__ == "__main__":
    main()