from utils import json_helper, constants
from argparse import ArgumentParser
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

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
def stats_analyze(stats_dict, period):

    df = pd.DataFrame(stats_dict).T
    df_period = df.tail(period)
    # print(df_period)

    summary_df = df_period.describe()
    print(summary_df)

    return summary_df

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

        cd_d_dict = stats_dict[constants.CD_D]
        ts_w_dict = stats_dict[constants.TS_W]

        stats_analyze(cd_d_dict, 7)
        # stats_analyze(cd_d_dict, 30)

        

if __name__ == "__main__":
    main()