from utils import json_helper, constants
from argparse import ArgumentParser
from pprint import pprint
import os
import logging
import pandas as pd

def calculate_avg(target_dict):
    df = pd.DataFrame(target_dict).T

    avg_df = df.diff() / 1.0
    # pprint(avg_df)
    avg_1_dict = avg_df.to_dict('index')

    avg_7_df = df.diff(7) / 7.0
    # pprint(avg_7_df)
    avg_7_dict = avg_7_df.to_dict('index')

    return avg_1_dict, avg_7_dict
    

def main():
    argparser = ArgumentParser(description="Dump stats on stats")
    argparser.add_argument("stats_file", help="repos_info stats files")
    args = argparser.parse_args()

    stats_file_list = []
    if args.stats_file == "all":
        all_stats_file_path = constants.REPOS_INFO_STATS_PATH
        stats_file_list = os.listdir(all_stats_file_path)
        suffix_len = len(constants.STATS_SUFFIX + constants.JSON_SUFFIX)
        stats_file_list = [stats_file[:-suffix_len] for stats_file in stats_file_list]
    else:
        stats_file_list.append(args.stats_file)
    
    for stats_file in stats_file_list:
        print(f"Getting stats_stats on {stats_file}")
        stats_file_path = constants.REPOS_INFO_STATS_PATH + stats_file + constants.STATS_SUFFIX + constants.JSON_SUFFIX

        stats_dict = json_helper.read_json(stats_file_path)
        cd_over_day_dict = stats_dict.get("cd_d")
        cd_d_d, cd_d_7_avg = calculate_avg(cd_over_day_dict)
        cd_over_week_dict = stats_dict.get("ts_w")
        ts_w_d, ts_w_7_avg = calculate_avg(cd_over_week_dict)

        stats_stats_filename = stats_file + constants.STATS_SUFFIX + constants.STATS_SUFFIX + '.json'
        stats_stats_full_path = constants.REPOS_INFO_STATS_STATS_PATH + stats_stats_filename
        stats_stats_dict = {
               constants.CD_D_D: cd_d_d,
               constants.CD_D_7_AVG: cd_d_7_avg,
               constants.TS_W_D: ts_w_d,
               constants.TS_W_7_AVG: ts_w_7_avg
        }

        json_helper.save_json(stats_stats_full_path, stats_stats_dict)


if __name__ == "__main__":
    main()