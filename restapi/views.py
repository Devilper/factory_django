import time


def get_user_info(request):
    user = getattr(request, "user", None)

    if user:
        return user
    else:
        return {}


def int_time_to_str(time_stamp):
    time_array = time.localtime(time_stamp)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)

    return time_str


def str_time_to_int(time_str):
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def datetime_to_int(date_time):
    return int(time.mktime(date_time.timetuple()))
