from utils import json_helper
from argparse import ArgumentParser
from pprint import pprint
import os
import logging
import pandas as pd

log = logging.getLogger()

# Set threshold of logger to info
log.setLevel(logging.INFO)

REPOS_INFO_PATH = "../repos_info/"
REPOS_INFO_METADATA_PATH = REPOS_INFO_PATH + "auth_metadata/"
REPOS_INFO_STATS_PATH = REPOS_INFO_PATH + "stats/"
COUNT_KEYS = ["forks_count", "stargazers_count", "watchers_count", "contributor_count", "subscribers_count", "committers_count"]


def fill_in_missing_dates(counts_metadata_dict):
    pass

# Function to perform statistical analysis of counts
def stats_log(counts_metadata_dict):

    df = pd.DataFrame(counts_metadata_dict).T
    print(df)

    summary_stats_df = df.describe()
    variance_df = df.var().to_frame('variance').T
    median_df = df.median().to_frame('median').T
    summary_stats_df = pd.concat([summary_stats_df, variance_df])
    summary_stats_df = pd.concat([summary_stats_df, median_df])
    pprint(summary_stats_df)
    summary_stats_dict = summary_stats_df.to_dict('index')

    rate_of_change_per_day_df = df.diff() / 1.0
    pprint(rate_of_change_per_day_df)
    rate_of_change_per_day_dict = rate_of_change_per_day_df.to_dict('index')

    rate_of_change_per_week_df = df.diff(7) / 7.0
    pprint(rate_of_change_per_week_df)
    rate_of_change_per_week_dict = rate_of_change_per_week_df.to_dict('index')

    return summary_stats_dict, rate_of_change_per_day_dict, rate_of_change_per_week_dict


def main():
    argparser = ArgumentParser(description="Dump stats on metadata")
    argparser.add_argument("metadata_dir", help="repos_info directory with metadata files")
    args = argparser.parse_args()

    metadata_dir = args.metadata_dir
    metadata_dir_path = REPOS_INFO_METADATA_PATH + metadata_dir + '/'
    metadata_files_list = sorted(os.listdir(metadata_dir_path))
    
    metadata_json_repo_count_dict = dict()
    for filename in metadata_files_list:
        filename_noext = os.path.splitext(filename)[0]
        filename_date = filename_noext[-8:]
        filename_fullpath = metadata_dir_path + '/' + filename

        raw_metadata_dict = json_helper.read_json(filename_fullpath)
        counts_dict = {key:value for key,value in raw_metadata_dict.items() if key in COUNT_KEYS}
        
        metadata_json_repo_count_dict[filename_date] = counts_dict
        
    summary_stats_dict, rate_of_change_per_day_dict, rate_of_change_per_week_dict = stats_log(metadata_json_repo_count_dict)
    # pprint(rate_of_change_per_day_dict)

    stats_filename = metadata_dir + '___stats.json'
    stats_full_path = REPOS_INFO_STATS_PATH + stats_filename
    stats_dict = {
        "summary_stats": summary_stats_dict,
        "rate_of_change_per_day": rate_of_change_per_day_dict,
        "rate_of_change_per_week": rate_of_change_per_week_dict
    }
    json_helper.save_json(stats_full_path, stats_dict)


if __name__ == "__main__":
    main()