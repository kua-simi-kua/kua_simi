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
REPOS_INFO_STATS_STATS_PATH = REPOS_INFO_PATH + "stats_stats/"
COUNT_KEYS = ["forks_count", "stargazers_count", "contributor_count", "subscribers_count", "committers_count"]


def get_data_at_date(target_dict, date=None):
    if date:
        return target_dict[date]
    else:
        sorted_dict_keys = sorted(target_dict.keys())
        max_key = sorted_dict_keys[-1]
        return target_dict[max_key]
    
def stats_agg_at_date(stats_file_list, date=None):
    all_rocd_dict, all_rocw_dict = dict(), dict()
    for stats_file in stats_file_list:
        stats_repo_name = stats_file[:-13]
        stats_file_path = REPOS_INFO_STATS_PATH + stats_file
        stats_file_dict = json_helper.read_json(stats_file_path)

        stats_file_rocd_dict = stats_file_dict["rocd"]
        all_rocd_dict[stats_repo_name] = get_data_at_date(stats_file_rocd_dict, date)

        stats_file_rocw_dict = stats_file_dict["rocw"]
        all_rocw_dict[stats_repo_name] = get_data_at_date(stats_file_rocw_dict, date)

    return all_rocd_dict, all_rocw_dict

def stats_stats_agg_at_date(stats_stats_file_list, date=None):
    all_ddrocd_dict, all_dwrocd_dict, all_ddrocw_dict, all_dwrocw_dict = [dict() for _ in range(4)]
    for stats_stats_file in stats_stats_file_list:
        stats_stats_repo_name = stats_stats_file[:-21]
        stats_stats_file_path = REPOS_INFO_STATS_STATS_PATH + stats_stats_file
        stats_stats_file_dict = json_helper.read_json(stats_stats_file_path)

        stats_stats_file_ddrocd_dict = stats_stats_file_dict["ddrocd"]
        all_ddrocd_dict[stats_stats_repo_name] = get_data_at_date(stats_stats_file_ddrocd_dict, date)

        stats_stats_file_dwrocd_dict = stats_stats_file_dict["dwrocd"]
        all_dwrocd_dict[stats_stats_repo_name] = get_data_at_date(stats_stats_file_dwrocd_dict, date)
        
        stats_stats_file_ddrocw_dict = stats_stats_file_dict["ddrocw"]
        all_ddrocw_dict[stats_stats_repo_name] = get_data_at_date(stats_stats_file_ddrocw_dict, date)

        stats_stats_file_dwrocw_dict = stats_stats_file_dict["dwrocw"]
        all_dwrocw_dict[stats_stats_repo_name] = get_data_at_date(stats_stats_file_dwrocw_dict, date)
    
    return all_ddrocd_dict, all_dwrocd_dict, all_ddrocw_dict, all_dwrocw_dict

def summary_stats(target_dict):
    df = pd.DataFrame.from_dict(target_dict, orient='index')
    return df.describe()


def main():

    # find the highest rocd and rocw
    # find the highest ddrocd, dwrocd, ddrocw, dwrocw

    stats_file_list = os.listdir(REPOS_INFO_STATS_PATH)
    all_rocd_dict, all_rocw_dict = stats_agg_at_date(stats_file_list)

    stats_stats_file_list = os.listdir(REPOS_INFO_STATS_STATS_PATH)
    all_ddrocd_dict, all_dwrocd_dict, all_ddrocw_dict, all_dwrocw_dict = stats_stats_agg_at_date(stats_stats_file_list)

    print(f"rocd summary: \n{summary_stats(all_rocd_dict)}")
    print(f"rocw summary: \n{summary_stats(all_rocw_dict)}")
    print(f"ddrocd summary: \n{summary_stats(all_ddrocd_dict)}")
    print(f"dwrocd summary: \n{summary_stats(all_dwrocd_dict)}")
    print(f"ddrocw summary: \n{summary_stats(all_ddrocw_dict)}")
    print(f"dwrocw summary: \n{summary_stats(all_dwrocw_dict)}")
        


if __name__ == "__main__":
    main()