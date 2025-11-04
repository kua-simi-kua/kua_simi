from utils import json_helper, constants, SpaceLaunchPad
from argparse import ArgumentParser
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def trend_slope(y):
    x = np.arange(len(y)).reshape(-1, 1)  # Independent variable (0, 1, ..., n-1)
    linear_regression_model = LinearRegression()
    linear_regression_model.fit(x, y)
    return linear_regression_model.coef_[0]  # Return the slope


def fill_in_missing_dates(counts_metadata_df):
    index_list = sorted(counts_metadata_df.index.to_list())
    if not len(index_list): # no metadata files i.e. repo has become inaccessible
        return pd.DataFrame()
    
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
def stats_log(counts_metadata_dict, stats_dict):

    df = pd.DataFrame(counts_metadata_dict).T
    df = fill_in_missing_dates(df)
    if df.empty: # empty df i.e. repo has become inaccessible 
        return dict()

    change_per_day_df = df.diff() / 1.0
    change_per_day_dict = change_per_day_df.to_dict('index')
    stats_dict[constants.CD].update(change_per_day_dict)

    trend_slope_over_week_df = pd.DataFrame(index=df.index)
    for count_key in constants.COUNT_KEYS:
        trend_slope_over_week_df[count_key] = df[count_key].rolling(window=7).apply(trend_slope, raw=True)
    trend_slope_over_week_dict = trend_slope_over_week_df.to_dict('index')
    stats_dict[constants.TSW].update(trend_slope_over_week_dict)

    return stats_dict

def main():
    argparser = ArgumentParser(description="Dump stats on metadata")
    argparser.add_argument("metadata_dir", help="repos_info directory with metadata files")
    argparser.add_argument("--do_token", "-dt", help="DigitalOcean Key ID and Key Secret", nargs=2, default=None)
    args = argparser.parse_args()

    metadata_dir_list = []
    if args.metadata_dir == "all":
        all_metadata_dir_path = constants.REPOS_INFO_METADATA_PATH
        metadata_dir_list = os.listdir(all_metadata_dir_path)
    else:
        metadata_dir_list.append(args.metadata_dir)

    do_token_list = args.do_token
    space_launch_pad = SpaceLaunchPad.SpaceLaunchPad(do_token_list[0], do_token_list[1])
    
    for metadata_dir in metadata_dir_list:
        print(f"Getting stats on {metadata_dir}")

        stats_filename = metadata_dir + constants.STATS_SUFFIX + constants.JSON_SUFFIX
        stats_full_path = constants.REPOS_INFO_STATS_PATH + stats_filename
        print(f"reading {stats_full_path}")
        stats_dict = json_helper.read_json(stats_full_path)

        if not stats_dict or not len(stats_dict):
            stats_dict = {
                constants.CD: {},
                constants.TSW: {},
            }
        
        # latest_recorded_date = get_latest_recorded_date(stats_dict)
        metadata_dir_path = constants.REPOS_INFO_METADATA_PATH + metadata_dir + '/'
        metadata_files_list = sorted(os.listdir(metadata_dir_path))
        
        metadata_json_repo_count_dict = dict()
        for filename in metadata_files_list:
            filename_noext, filename_ext = os.path.splitext(filename)
            if filename_ext != constants.JSON_SUFFIX: continue
            filename_date = filename_noext[-8:]
            # print(f"reading {filename}")
            
            filename_fullpath = metadata_dir_path + '/' + filename
            raw_metadata_dict = json_helper.read_json(filename_fullpath)
            counts_dict = {key:value for key,value in raw_metadata_dict.items() if key in constants.COUNT_KEYS}
            metadata_json_repo_count_dict[filename_date] = counts_dict
            
        stats_updated_dict = stats_log(metadata_json_repo_count_dict, stats_dict)
        if len(stats_updated_dict):
            json_helper.save_json(stats_full_path, stats_updated_dict)
            do_key = stats_full_path[3:] # remove `../` from the stats_full_path
            space_launch_pad.launch_to_space(key=do_key, file_path=stats_full_path)


if __name__ == "__main__":
    main()