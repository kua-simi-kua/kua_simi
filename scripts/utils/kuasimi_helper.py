from utils import json_helper, constants, datetime_helper
import datetime
import os

CONFIG_ALL_REPOS_PATH = "../config/repos_list_long.json"

def get_repo_slash_string_from_url(repo_url):
    """
    Given a repo URL https://github.com/USER/REPO , return the repo slash string USER/REPO .
    This is needed for the Github object to query the API for the repo.
    """
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

def get_repo_string_from_slash_string(repo_slash_string):
    """
    Given a repo slash string USER/REPO, return the repo string USER___REPO.
    """
    repo_string_token_list = repo_slash_string.split("/")
    repo_string = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    return repo_string

def get_all_repo_strings():
    """
    Return all repos currently tracked in repos_list_long.json.
    """
    all_repos_list = json_helper.read_json(CONFIG_ALL_REPOS_PATH)
    all_repo_strings_list = [get_repo_string_from_slash_string(
        get_repo_slash_string_from_url(repo_url)
        ) for repo_url in all_repos_list]
    return all_repo_strings_list

def get_metadata_files(launch_pad, repo_name, start_days=8):
    """
    Getting metadata files from Space
    Return list of local metadata file locations. 
    """
    today = datetime.date.today()
    date_list = [datetime_helper.get_string_YYYYMMDD(today - datetime.timedelta(days=i)) for i in range(start_days)]
    local_filename_list = []

    # creates repo_dir if repo_dir does not exist, so file can be created smoothly
    repo_dir = f"{constants.REPOS_INFO_METADATA_PATH}{repo_name}"
    if not os.path.isdir(repo_dir):
        os.makedirs(repo_dir)

    for date_str in date_list:
        try:
            local_filepath = f"{repo_dir}/{repo_name}___{date_str}{constants.JSON_SUFFIX}"
            space_filename = local_filepath[3:]
            print(f"getting {space_filename}")
            launch_pad.get_from_space(space_filename, local_filepath)
            print(f"Parking into {local_filepath}")
            local_filename_list.append(local_filepath)
        except Exception as e:
            print(f"having trouble pulling {space_filename}")
            print(e)
    return local_filename_list

def get_stats_files(space_launch_pad, repo_name):
    """
    Getting stats files from space
    Return local stats file location and space location
    """
    local_filepath = f"{constants.REPOS_INFO_STATS_PATH}{repo_name}___stats{constants.JSON_SUFFIX}"
    space_filename = local_filepath[3:]
    try:
        print(f"getting {space_filename}")
        space_launch_pad.get_from_space(space_filename, local_filepath)
        print(f"Parking into {local_filepath}")
    except Exception as e:
        print(f"having trouble pulling {space_filename}")
        print(e)
    return local_filepath, space_filename

def get_stats_stats_files(space_launch_pad, repo_name):
    """
    Getting stats_stats files from space
    Return local stats_stats file location and space location.
    """
    local_filepath = f"{constants.REPOS_INFO_STATS_STATS_PATH}{repo_name}___stats___stats{constants.JSON_SUFFIX}"
    space_filename = local_filepath[3:]
    try:
        print(f"getting {space_filename}")
        space_launch_pad.get_from_space(space_filename, local_filepath)
        print(f"Parking into {local_filepath}")
    except Exception as e:
        print(f"having trouble pulling {space_filename}")
        print(e)
    return local_filepath, space_filename

def get_alert_files(space_launch_pad, repo_name):
    """
    Getting alert files from space
    Return list of local alert file locations
    """
    local_dir = f"{constants.REPOS_INFO_ALERTS_PATH}{repo_name}"
    local_filename_list = []

    # creates local_dir if local_dir does not exist, so file can be created smoothly
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)

    for count_key in constants.COUNT_KEYS:
        filename = f"{count_key}{constants.JSON_SUFFIX}"
        local_filename = f"{local_dir}/{filename}"
        space_filename = local_filename[3:] 
        try: 
            space_launch_pad.get_from_space(space_filename, local_filename)
            local_filename_list.append(local_filename)
        except Exception as e:
            print(f"having trouble pulling {space_filename}")
            print(e)
    return local_filename_list

def view_recent_alerts(alertfile, start_time=30):
    """
    View alerts in an alert file, dating back to a specified start time.  
    """
    alerts = json_helper.read_json(alertfile)
    today = datetime.date.today()
    start_date = datetime_helper.get_string_YYYYMMDD(today - datetime.timedelta(days=start_time))
    recent_alerts = {k: v for k, v in alerts.items() if k > start_date}
    return recent_alerts