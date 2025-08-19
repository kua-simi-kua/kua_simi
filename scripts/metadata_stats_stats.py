from metadata_stats import *

def stats_stats_log(target_dict):
    df = pd.DataFrame(target_dict).T

    change_per_day_df = df.diff() / 1.0
    change_per_day_dict = change_per_day_df.to_dict('index')

    # avg_7_df = df.diff(7) / 7.0
    # # pprint(avg_7_df)
    # avg_7_dict = avg_7_df.to_dict('index')

    trend_slope_over_week_df = pd.DataFrame(index=df.index)
    for count_key in constants.COUNT_KEYS:
        trend_slope_over_week_df[count_key] = df[count_key].rolling(window=7).apply(trend_slope, raw=True)
    trend_slope_over_week_dict = trend_slope_over_week_df.to_dict('index')

    return change_per_day_dict, trend_slope_over_week_dict

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
        cd_over_day_dict = stats_dict.get(constants.CD)
        cd_cd, cd_tsw = stats_stats_log(cd_over_day_dict)
        cd_over_week_dict = stats_dict.get(constants.TSW)
        tsw_cd, tsw_tsw = stats_stats_log(cd_over_week_dict)

        stats_stats_filename = stats_file + constants.STATS_SUFFIX + constants.STATS_SUFFIX + '.json'
        stats_stats_full_path = constants.REPOS_INFO_STATS_STATS_PATH + stats_stats_filename
        stats_stats_dict = {
               constants.CD_CD: cd_cd,
               constants.CD_TSW: cd_tsw,
               constants.TSW_CD: tsw_cd,
               constants.TSW_TSW: tsw_tsw
        }

        json_helper.save_json(stats_stats_full_path, stats_stats_dict)


if __name__ == "__main__":
    main()