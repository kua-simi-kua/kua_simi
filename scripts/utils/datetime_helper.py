from datetime import datetime, timedelta

def get_string_YYYYMMDD(datetime_obj:datetime) -> str:
    return datetime_obj.strftime("%Y%m%d")

def get_string_YYYYMMDD_HHMMSS_UTC(datetime_obj:datetime) -> str:
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S UTC")

def get_datetime_from_YYYYMMDD(datetime_str:str) -> datetime:
    return datetime.strptime(datetime_str, "%Y%m%d")

def get_datetime_from_YYYYMMDD_HHMMSS_UTC(datetime_str:str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S UTC")

def is_within_timedelta_hours(datetime_str_a:str, datetime_str_b:str, time_diff_hours:int) -> bool:
    datetime_a = get_datetime_from_YYYYMMDD_HHMMSS_UTC(datetime_str_a)
    datetime_b = get_datetime_from_YYYYMMDD_HHMMSS_UTC(datetime_str_b)
    return abs(datetime_a - datetime_b) <= timedelta(hours = time_diff_hours)