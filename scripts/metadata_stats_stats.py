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
REPOS_INFO_STATS_PATH = REPOS_INFO_PATH + "stats/"
REPOS_INFO_STATS_STATS_PATH = REPOS_INFO_PATH + "stats_stats/"
STATS_SUFFIX = '___stats'
JSON_SUFFIX = '.json'



def calculate_derivative(target_dict):
    df = pd.DataFrame(target_dict).T

    summary_stats_df = df.describe()
    variance_df = df.var().to_frame('variance').T
    median_df = df.median().to_frame('median').T
    summary_stats_df = pd.concat([summary_stats_df, variance_df])
    summary_stats_df = pd.concat([summary_stats_df, median_df])
    # pprint(summary_stats_df)
    summary_stats_dict = summary_stats_df.to_dict('index')

    derivative_df = df.diff() / 1.0
    # pprint(derivative_df)
    derivative_1_dict = derivative_df.to_dict('index')

    derivative_7_df = df.diff(7) / 7.0
    # pprint(derivative_7_df)
    derivative_7_dict = derivative_7_df.to_dict('index')

    return summary_stats_dict, derivative_1_dict, derivative_7_dict


def main():
    argparser = ArgumentParser(description="Dump stats on stats")
    argparser.add_argument("stats_file", help="repos_info stats files")
    args = argparser.parse_args()

    stats_file_list = []
    if args.stats_file == "all":
        all_stats_file_path = REPOS_INFO_STATS_PATH
        stats_file_list = os.listdir(all_stats_file_path)
        suffix_len = len(STATS_SUFFIX + JSON_SUFFIX)
        stats_file_list = [stats_file[:-suffix_len] for stats_file in stats_file_list]
    else:
        stats_file_list.append(args.stats_file)
    
    for stats_file in stats_file_list:
        print(f"Getting stats on {stats_file}")
        stats_file_path = REPOS_INFO_STATS_PATH + stats_file + STATS_SUFFIX + JSON_SUFFIX

        stats_dict = json_helper.read_json(stats_file_path)
        rate_of_change_per_day_dict = stats_dict.get("rate_of_change_per_day")
        summary_stats_roc_per_day_dict, derivative_1_roc_per_day_dict, derivative_7_roc_per_day_dict = calculate_derivative(rate_of_change_per_day_dict)
        rate_of_change_per_week_dict = stats_dict.get("rate_of_change_per_week")
        summary_stats_roc_per_week_dict, derivative_1_roc_per_week_dict, derivative_7_roc_per_week_dict = calculate_derivative(rate_of_change_per_week_dict)

        stats_stats_filename = stats_file + STATS_SUFFIX + STATS_SUFFIX + '.json'
        stats_stats_full_path = REPOS_INFO_STATS_STATS_PATH + stats_stats_filename
        stats_stats_dict = {
               "summary_stats_roc_per_day": summary_stats_roc_per_day_dict,
               "derivative_1_roc_per_day": derivative_1_roc_per_day_dict,
               "derivative_7_roc_per_day": derivative_7_roc_per_day_dict,
               "summary_stats_roc_per_week": summary_stats_roc_per_week_dict,
               "derivative_1_roc_per_week": derivative_1_roc_per_week_dict,
               "derivative_7_roc_per_week": derivative_7_roc_per_week_dict
        }

        json_helper.save_json(stats_stats_full_path, stats_stats_dict)


if __name__ == "__main__":
    main()