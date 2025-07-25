from utils import json_helper, constants
from argparse import ArgumentParser
import os
import pandas as pd
import numpy as np
from pprint import pprint

def fill_in_missing_dates(counts_metadata_df):
    index_list = sorted(counts_metadata_df.index.to_list())
    
    start_date = index_list[0]
    end_date = index_list[-1]
    full_date_range = pd.date_range(start=start_date, end=end_date).to_list()
    full_date_range = [datetimestamp.strftime("%Y%m%d") for datetimestamp in full_date_range]

    for date_string in full_date_range:
        if date_string not in index_list:
            counts_metadata_df.loc[date_string] = [float('nan')] * len(constants.COUNT_KEYS)
    
    counts_metadata_df.sort_index(inplace=True)
    counts_metadata_df.interpolate(method="linear", inplace=True)
    return counts_metadata_df

def stats_summary(stats_dict, period, target_date=None):
    stats_df = pd.DataFrame(stats_dict).T

    if target_date and target_date in stats_df.index:
        stats_df = stats_df[stats_df.index <= target_date]
    df_period = stats_df.tail(period)

    summary_df = df_period.describe()
    summary_dict = summary_df.to_dict()
    return df_period, summary_df, summary_dict

def stats_summary_compare(summary_dict, stats_df):
    target_row_dict = stats_df.tail(1).to_dict()
    target_date = stats_df.index[-1]
    alert_row_dict = {}
    for count_key in constants.COUNT_KEYS:
        if target_row_dict[count_key][target_date] > summary_dict[count_key]['75%']:
            alert_row_dict[count_key] = {
                'target': target_row_dict[count_key][target_date],
                '75': summary_dict[count_key]['75%']
            }
    return alert_row_dict

def main():
    argparser = ArgumentParser(description="Dump stats on metadata")
    argparser.add_argument("metadata_dir", help="repos_info directory with metadata files")
    argparser.add_argument("-td", "--target-date", help="target date to compare stats", nargs="?", default=None)
    argparser.add_argument("-l", "--log-file", help="log file to log alerts", nargs="?", default="")
    args = argparser.parse_args()

    if len(args.log_file):
        alerts_dict = json_helper.read_json(args.log_file)
        if not alerts_dict:
            alerts_dict = dict()

    metadata_dir_list = []
    if args.metadata_dir == "all":
        all_metadata_dir_path = constants.REPOS_INFO_METADATA_PATH
        metadata_dir_list = os.listdir(all_metadata_dir_path)
    else:
        metadata_dir_list.append(args.metadata_dir)

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

        if args.log_file:
            target_date = cd_df_7.index[-1]
            target_date_dict = dict()
            check_list = [
                ('cd_7', stats_summary_compare(cd_7_summary, cd_df_7)),
                ('cd_30', stats_summary_compare(cd_30_summary, cd_df_30)),
                ('tsw_7', stats_summary_compare(tsw_7_summary, tsw_df_7)),
                ('tsw_30', stats_summary_compare(tsw_30_summary, tsw_df_30))
            ]
            for key, func in check_list:
                if func: target_date_dict[key] = func
            
            if len(target_date_dict):
                if metadata_dir in alerts_dict:
                    alerts_dict[metadata_dir].update({target_date: target_date_dict})
                else:
                    alerts_dict[metadata_dir] = {target_date: target_date_dict}
            
            json_helper.save_json(args.log_file, alerts_dict)
        else:
            continue
        


        

        

if __name__ == "__main__":
    main()