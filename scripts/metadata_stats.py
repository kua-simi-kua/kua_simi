from utils import json_helper, constants
from argparse import ArgumentParser
from pprint import pprint
import os
import logging
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

log = logging.getLogger()

# Set threshold of logger to info
log.setLevel(logging.INFO)


def trend_slope(y):
    x = np.arange(len(y)).reshape(-1, 1)  # Independent variable (0, 1, ..., n-1)
    linear_regression_model = LinearRegression()
    linear_regression_model.fit(x, y)
    return linear_regression_model.coef_[0]  # Return the slope


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


# Function to perform statistical analysis of counts
def stats_log(counts_metadata_dict):

    df = pd.DataFrame(counts_metadata_dict).T
    # summary_stats_df = df.describe()
    # variance_df = df.var().to_frame('variance').T
    # median_df = df.median().to_frame('median').T
    # summary_stats_df = pd.concat([summary_stats_df, variance_df])
    # summary_stats_df = pd.concat([summary_stats_df, median_df])
    # # pprint(summary_stats_df)
    # summary_stats_dict = summary_stats_df.to_dict('index')

    df = fill_in_missing_dates(df)

    change_per_day_df = df.diff() / 1.0
    change_per_day_dict = change_per_day_df.to_dict('index')

    trend_slope_over_week_df = pd.DataFrame(index=df.index)
    for count_key in constants.COUNT_KEYS:
        trend_slope_over_week_df[count_key] = df[count_key].rolling(window=7).apply(trend_slope, raw=True)
    trend_slope_over_week_dict = trend_slope_over_week_df.to_dict('index')

    return change_per_day_dict, trend_slope_over_week_dict


def main():
    argparser = ArgumentParser(description="Dump stats on metadata")
    argparser.add_argument("metadata_dir", help="repos_info directory with metadata files")
    args = argparser.parse_args()

    metadata_dir_list = []
    if args.metadata_dir == "all":
        all_metadata_dir_path = constants.REPOS_INFO_METADATA_PATH
        metadata_dir_list = os.listdir(all_metadata_dir_path)
    else:
        metadata_dir_list.append(args.metadata_dir)
    
    for metadata_dir in metadata_dir_list:
        print(f"Getting stats on {metadata_dir}")

        stats_filename = metadata_dir + constants.STATS_SUFFIX + constants.JSON_SUFFIX
        stats_full_path = constants.REPOS_INFO_STATS_PATH + stats_filename
        print(f"reading {stats_full_path}")
        stats_dict = json_helper.read_json(stats_full_path)

        if not stats_dict:
            stats_dict = {
                "cd_d": {},
                "ts_w": {},
            }

        metadata_dir_path = constants.REPOS_INFO_METADATA_PATH + metadata_dir + '/'
        metadata_files_list = sorted(os.listdir(metadata_dir_path))
        
        metadata_json_repo_count_dict = dict()
        for filename in metadata_files_list:
            filename_noext, filename_ext = os.path.splitext(filename)
            if filename_ext != constants.JSON_SUFFIX: continue
            print(f"reading {filename}")
            filename_date = filename_noext[-8:]
            
            filename_fullpath = metadata_dir_path + '/' + filename
            raw_metadata_dict = json_helper.read_json(filename_fullpath)
            counts_dict = {key:value for key,value in raw_metadata_dict.items() if key in constants.COUNT_KEYS}
            metadata_json_repo_count_dict[filename_date] = counts_dict
            
        # summary_stats_dict, 
        change_per_day_dict, trend_slope_over_week_dict = stats_log(metadata_json_repo_count_dict)
        # pprint(trend_slope_over_week_dict)

        stats_dict["cd_d"].update(change_per_day_dict)
        stats_dict["ts_w"].update(trend_slope_over_week_dict)
        json_helper.save_json(stats_full_path, stats_dict)


if __name__ == "__main__":
    main()