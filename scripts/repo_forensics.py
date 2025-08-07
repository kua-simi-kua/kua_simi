import os
import re
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
from pprint import pprint

from utils import json_helper, constants

def extract_date_from_filename(filename):
    match = re.search(r'(\d{8})\.json$', filename)
    if match:
        return datetime.strptime(match.group(1), "%Y%m%d")
    return None

def process_json_files(directory):
    data_by_key = defaultdict(list)
    for filename in os.listdir(directory):
        if not filename.endswith(constants.JSON_SUFFIX): continue
        file_date = extract_date_from_filename(filename)
        if not file_date: continue
        full_path = os.path.join(directory, filename)
        try:
            content = json_helper.read_json(full_path)
            for key, value in content.items():
                if key in constants.COUNT_KEYS:
                    data_by_key[key].append((file_date, value))
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
    return data_by_key

def plot_counts(data_by_key, start_time, count_key_list):
    colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_counter = 0
    for key, entries in data_by_key.items():
        if key not in count_key_list: continue
        plt.figure()
        dates, counts = zip(*sorted(entries))
        plt.plot(dates[-start_time:], counts[-start_time:], marker='o', linestyle='-', label=key, color=colours[colour_counter])
        colour_counter += 1
        plt.title(f"{key} Over Time")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.legend()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot counts for each repo")
    parser.add_argument("repo_name", help="Repo Name in USER___REPO format")
    parser.add_argument("-st", "--start-time", help="Start time for graph plotting",default=30, nargs="?")
    parser.add_argument("-k", "--count-key", help="Count keys to examine", default="all", nargs='*')
    args = parser.parse_args()

    repo_alerts_dir = constants.REPOS_INFO_ALERTS_PATH + args.repo_name + "/"
    count_key_list = args.count_key
    if count_key_list == 'all': count_key_list = constants.COUNT_KEYS

    for count_key in count_key_list:
        repo_alerts_filepath = repo_alerts_dir + count_key + constants.JSON_SUFFIX
        alerts = json_helper.read_json(repo_alerts_filepath)
        print(f"\n{repo_alerts_filepath}")
        pprint(alerts)

    repo_metadata_path = os.path.join(constants.REPOS_INFO_METADATA_PATH, args.repo_name)
    data = process_json_files(repo_metadata_path)
    plot_counts(data, args.start_time, count_key_list)

if __name__ == "__main__":
    main()