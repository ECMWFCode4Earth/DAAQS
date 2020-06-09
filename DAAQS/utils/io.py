import gzip
import json
import os
from datetime import datetime, timedelta

from tqdm import tqdm

from DAAQS.utils.constants import NO_DATA_DICT


def _read_gzip_file(path):

    with gzip.GzipFile(path, "r") as jsonzip:
        data = []

        for each_json in jsonzip:
            single_dict = json.loads(each_json)

            try:
                oaq = OpenaqData(single_dict)
            except KeyError:
                oaq = OpenaqData(NO_DATA_DICT)
            finally:
                data.append(oaq)
    return data


def read_opeaq_day(path):

    file_list = [x for x in os.listdir(path)]
    data = []
    for each in file_list:
        fpath = path + each
        data.extend(_read_gzip_file(fpath))
    return data


def read_openaq_year(data_path, year):

    """
    The function is not advisable due to the time it can take,
    though is working without a bug.
    """

    daily_list = _generate_daily_list(year)
    print("Overriding daily list. The following line should be commented")
    print("The year now has only 3 random days for testing")

    daily_list = ["2018-01-01", "2018-06-05", "2018-07-18"]

    data = []
    for each_day in daily_list:
        day_path = data_path + each_day
        data.extend(read_opeaq_day(day_path))
        print(f"Read the data for {each_day}")

    return data


def _generate_daily_list(year):

    strt_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    num_days = end_date - strt_date

    daily_list = []
    for day in range(num_days.days):
        dt = strt_date + timedelta(days=day)
        dt_str = dt.strftime("%Y-%m-%d")
        daily_list.append(dt_str + "/")

    return daily_list


def loc_lat_lon(path, year, parameter):
    """

    The parameters can be:
    pm25
    pm10
    so2
    no2
    o3
    co
    bc
    None
    """
    # Uncomment later
    # daily_list = _generate_daily_list(year)

    # Comment Later
    print("Overriding daily list. The following line should be commented")
    print("The year year has 3 random days for testing")
    daily_list = ["2018-01-01/", "2018-06-05/", "2018-07-18/"]

    loc_lat_lon = set()
    for each in tqdm(daily_list):
        daily_path = path + each
        data = read_opeaq_day(daily_path)
        for each in data:
            if each.parameter == parameter:
                loc_lat_lon.add((each.location, each.lat, each.lon))

    return loc_lat_lon


class OpenaqData(object):
    """
    The class stores the raw json value of openAQ data
    """

    __slots__ = (
        "location",
        "time",
        "parameter",
        "value",
        "unit",
        "avg_time",
        "avg_time_unit",
        "lat",
        "lon",
    )

    def __init__(self, json_dict):
        """
        Standardised storage for data.
        Time is always stored  in 'UTC'
        Standard units are as follows:

        PM10 = ug/m3
        Ozone =
        SO2 =
        averaging time is in hoursq
        """
        self.location = json_dict["location"]
        time = json_dict["date"]["utc"]
        self.time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.parameter = json_dict["parameter"]
        self.value = json_dict["value"]
        self.unit = json_dict["unit"]
        self.avg_time = json_dict["averagingPeriod"]["value"]
        self.avg_time_unit = json_dict["averagingPeriod"]["unit"]
        self.lat = json_dict["coordinates"]["latitude"]
        self.lon = json_dict["coordinates"]["longitude"]


# def write_h5py(data_path, write_path):
