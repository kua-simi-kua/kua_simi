from utils import json_helper
import os
import logging
import pandas as pd

log = logging.getLogger()

# Set threshold of logger to info
log.setLevel(logging.INFO)

REPOS_INFO_PATH = "../repos_info/auth_metadata/"
GITHUB_METADATA_JSON_PREFIX = "github_metadata___"
GITHUB_METADATA_STATS_JSON_PREFIX = "github_metadata_stats___"

# Function to retrieve a list of metadata_json_files
def enumerate_metadata_json_files(directory_path):
    metadata_json_files = []
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is one of the metadata files of interest
        if filename.startswith(f"{GITHUB_METADATA_JSON_PREFIX}"):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)
            metadata_json_files.append(file_path)
    if metadata_json_files:
        json_files_count = len(metadata_json_files)
        logging.info(f"Found {json_files_count} Github metadata json files")
        for metadata_json_file in metadata_json_files:
            logging.info(metadata_json_file)
    else:
        logging.info("No Github metadata json file found in the specified directory.")
    return metadata_json_files

# Function to retrieve a the full path and filename of the json file of interest
def obtain_collected_metadata_stats_filepath(json_file):
    delimiters = ["_", "___", ".", "/", "\\"]
    for delimiter in delimiters:
        json_file = " ".join(json_file.split(delimiter))
    json_file_token_list = json_file.split()
    metadata_filename = json_file_token_list[-3] + "__" + json_file_token_list[-2]
    metadata_full_file_path = os.path.join(REPOS_INFO_PATH, f"{GITHUB_METADATA_STATS_JSON_PREFIX}{metadata_filename}.json")
    print(metadata_filename)
    print(metadata_full_file_path)
    return metadata_full_file_path, metadata_filename

# Function to only retrieve the counts from the metadata json file
def filter_count_keys(metadata_dict):
    result = {}
    for key, value in metadata_dict.items():
        result[key] = {}
        for sub_key, sub_value in value.items():
            if sub_key.endswith('_count'):
                result[key][sub_key] = sub_value
    return result

# Function to perform statistical analysis of counts
def stats_log(counts_metadata_dict):

    df = pd.DataFrame(counts_metadata_dict).T
    print(df)

    # Calculate summary statistics
    summary_stats = df.describe().to_json(orient="index")
    print(summary_stats)

    # For additional statistical insights, let's also calculate the variance and median
    variance = df.var().to_json(orient="index")
    
    median = df.median().to_json(orient="index")
    # print(f"\nVariance:\n", variance)
    # print(f"\nMedian:\n", median)

    # Calculate the difference between consecutive rows
    diff_df = df.diff().to_json(orient="index")

    # Divide by the time period (7 days) to get the rate of change per day
    rate_of_change_df = (df.diff()/7).to_json(orient="index")


    # Display the rate of change DataFrame
    # print(f"\nRate of Change per Week:\n", rate_of_change_df)

    
    return summary_stats, variance, median, diff_df, rate_of_change_df

def main():
    # Enumerate github metadata json files in ../repos_info/auth_metadata
    directory_path = "../repos_info/auth_metadata"

    metadata_json_files = enumerate_metadata_json_files(directory_path)

    for metadata_json_file in metadata_json_files:
        metadata_dict = json_helper.read_json(metadata_json_file)
        if not metadata_json_file:
            logging.info(f"Metadata of {metadata_json_file}: Failed to extract.")
    
        counts_metadata_dict = filter_count_keys(metadata_dict)
    
        logging.info(f"Counts metadata: \n {counts_metadata_dict}")

        # Stats
        summary_stats, variance, median, diff_df, rate_of_change_df = stats_log(counts_metadata_dict)

        # Prep metadata_stats_filepath to store updated info
        # if metadata_stats_filepath does not exist, create empty dict to store info
        metadata_stats_full_file_path, metadata_stats_filename = obtain_collected_metadata_stats_filepath(metadata_json_file)
        metadata_stats_dict = json_helper.read_json(metadata_stats_full_file_path)
        if not metadata_stats_dict:
            metadata_stats_dict = {}

        metadata_stats_dict_data = {
            "summary_stats": summary_stats,
            "variance_stats": variance,
            "median_stats": median,
            "changes": diff_df,
            "rate_of_change_weekly": rate_of_change_df
        }
        metadata_stats_dict[metadata_stats_filename] = metadata_stats_dict_data
        json_helper.save_json(metadata_stats_full_file_path, metadata_stats_dict)

        logging.info(f"Finished calculating metadata statistics for {metadata_stats_filename}")

if __name__ == "__main__":
    main()