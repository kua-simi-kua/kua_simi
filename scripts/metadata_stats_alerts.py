from utils import json_helper, constants
from argparse import ArgumentParser
import os
import pandas as pd
import numpy as np
from pprint import pprint
from collections import defaultdict

def stats_summary(stats_dict, period, target_date=None):
    stats_df = pd.DataFrame(stats_dict).T

    if target_date and target_date in stats_df.index:
        stats_df = stats_df[stats_df.index <= target_date]
    df_period = stats_df.tail(period)

    summary_df = df_period.describe()
    summary_dict = summary_df.to_dict()
    return df_period, summary_df, summary_dict

def stats_summary_compare(dfsummary_list, repo_count_alerts_filepath, count_key):
    repo_count_alerts = json_helper.read_json(repo_count_alerts_filepath)
    if not repo_count_alerts: repo_count_alerts = {}
    repo_count_alerts = defaultdict(dict, repo_count_alerts)
    for alert_type, stats_df, summary_dict in dfsummary_list:
        target_row_dict = stats_df.tail(1).to_dict()
        target_date = stats_df.index[-1]
        if target_row_dict[count_key][target_date] > summary_dict[count_key]['75%']:
            repo_count_alerts[target_date][alert_type] = {
                'target': target_row_dict[count_key][target_date],
                '75': summary_dict[count_key]['75%']
            }
    repo_count_alerts = dict(repo_count_alerts)
    json_helper.save_json(repo_count_alerts_filepath, repo_count_alerts)
    print(f"written {repo_count_alerts_filepath}")

def main():
    argparser = ArgumentParser(description="Dump stats on metadata")
    argparser.add_argument("metadata_dir", help="repos_info directory with metadata files")
    argparser.add_argument("-td", "--target-date", help="target date to compare stats", nargs="?", default=None)
    args = argparser.parse_args()


    metadata_dir_list = []
    if args.metadata_dir == "all":
        all_metadata_dir_path = constants.REPOS_INFO_METADATA_PATH
        metadata_dir_list = os.listdir(all_metadata_dir_path)
    else:
        metadata_dir_list.append(args.metadata_dir)

    print(f"Examining target date of {args.target_date}")
    for metadata_dir in metadata_dir_list:
        print(f"Processing {metadata_dir}")

        stats_filename = metadata_dir + constants.STATS_SUFFIX + constants.JSON_SUFFIX
        stats_full_path = constants.REPOS_INFO_STATS_PATH + stats_filename
        stats_dict = json_helper.read_json(stats_full_path)
        if stats_dict:
            print(f"reading {stats_full_path}")
        else:
            print(f"{stats_full_path} is either non-existent or empty")
            continue

        cd_dict = stats_dict[constants.CD]
        tsw_dict = stats_dict[constants.TSW]

        cd_df_7, _, cd_7_summary = stats_summary(cd_dict, 7, args.target_date)
        cd_df_30, _, cd_30_summary = stats_summary(cd_dict, 30, args.target_date)
        tsw_df_7, _, tsw_7_summary = stats_summary(tsw_dict, 7, args.target_date)
        tsw_df_30, _, tsw_30_summary = stats_summary(tsw_dict, 30, args.target_date)
        dfsummary_list = [
            ('cd_7', cd_df_7, cd_7_summary),
            ('cd_30', cd_df_30, cd_30_summary),
            ('tsw_7', tsw_df_7, tsw_7_summary),
            ('tsw_30', tsw_df_30, tsw_30_summary)            
        ]

        repo_alerts_dir_path = constants.REPOS_INFO_ALERTS_PATH + metadata_dir + '/'
        os.makedirs(repo_alerts_dir_path, exist_ok=True)
        for count_key in constants.COUNT_KEYS:
            repo_count_alerts_filepath = repo_alerts_dir_path + count_key + constants.JSON_SUFFIX
            stats_summary_compare(dfsummary_list, repo_count_alerts_filepath, count_key)
        
if __name__ == "__main__":
    main()