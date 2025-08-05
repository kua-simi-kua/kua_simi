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

def is_count_key(key):
    # Customize this function if needed
    return 'count' in key.lower()

def process_json_files(directory):
    data_by_key = defaultdict(list)
    for filename in os.listdir(directory):
        if not filename.endswith('.json'):
            continue

        file_date = extract_date_from_filename(filename)
        if not file_date:
            continue

        full_path = os.path.join(directory, filename)
        try:
            content = json_helper.read_json(full_path)
            for key, value in content.items():
                if key in constants.COUNT_KEYS:
                    data_by_key[key].append((file_date, value))
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    return data_by_key

def plot_counts(data_by_key, start_time):
    colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_counter = 0
    for key, entries in data_by_key.items():
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
    args = parser.parse_args()

    repo_alerts_path = os.path.join(constants.REPOS_INFO_ALERTS_PATH, args.repo_name + constants.JSON_SUFFIX)
    repo_alerts = json_helper.read_json(repo_alerts_path)
    most_recent_alert_dates = list(repo_alerts.keys())[-30:]
    most_recent_alerts = {date : repo_alerts[date] for date in most_recent_alert_dates}
    pprint(most_recent_alerts)

    repo_metadata_path = os.path.join(constants.REPOS_INFO_METADATA_PATH, args.repo_name)
    data = process_json_files(repo_metadata_path)
    plot_counts(data, args.start_time)

if __name__ == "__main__":
    main()