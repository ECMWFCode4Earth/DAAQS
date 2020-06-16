import csv
import gzip
import json
import os
from datetime import datetime, timedelta

import h5py
import numpy as np
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


def read_openaq_day(path):
    # strt_time = time.time()
    file_list = [x for x in os.listdir(path) if x.split(".")[-1] == "gz"]
    data = []
    for each in file_list:
        fpath = path + each
        data.extend(_read_gzip_file(fpath))
    # print(f"The time taken to read one day is {time.time()-strt_time}")
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

    daily_list = _generate_daily_list(year)

    # Comment Later
    # print("Overriding daily list. The following line should be commented")
    # print("The year year has 3 random days for testing")
    # daily_list = ["2018-01-01/", "2018-06-05/", "2018-07-18/"]

    loc_lat_lon = set()
    for each in tqdm(daily_list):
        daily_path = path + each
        data = read_openaq_day(daily_path)
        for each in data:
            if each.parameter == parameter:
                loc_lat_lon.add((each.location, each.lat, each.lon))

    return loc_lat_lon


def write_lll(path, year, parameter):

    lll = loc_lat_lon(path, year, parameter)
    path = path + "loc_lat_lon/lll_" + year + "_" + parameter + ".csv"
    with open(path, "w") as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["loc", "lat", "lon"])
        for row in lll:
            csv_out.writerow(row)


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


def write_h5py(data_path, write_path, year: int):

    daily_list = _generate_daily_list(year)
    print("Overriding daily list. The following line should be commented")
    print("The year now has only 3 random days for testing")

    daily_list = ["2018-01-01/", "2018-06-05/", "2018-07-18/"]

    write_path = write_path + str(year) + ".h5"

    #  Initialising with a none type data

    with h5py.File(write_path, "w") as f:
        data = OpenaqData(NO_DATA_DICT)
        grp = data.location + "/" + data.parameter

        time = data.time.strftime("%Y/%M/%d %H:%M:%S")
        value = data.value
        unit = data.unit
        avg_time = data.avg_time
        avg_time_unit = data.avg_time_unit
        lat = data.lat
        lon = data.lon

        dtype = h5py.special_dtype(vlen=str)

        arr_data = np.array(
            [time, value, unit, avg_time, avg_time_unit, lat, lon], dtype=dtype
        ).reshape(1, 7)

        f.create_dataset(grp, data=arr_data, maxshape=(None, 7))

    with h5py.File(write_path, "a") as f:
        for each_day in tqdm(daily_list):
            day_path = data_path + each_day
            data = read_openaq_day(day_path)

            dtype = h5py.special_dtype(vlen=str)

            for each_data in data:

                if each_data.location is not None:
                    time = each_data.time.strftime("%Y/%M/%d %H:%M:%S")
                    value = each_data.value
                    unit = each_data.unit
                    avg_time = each_data.avg_time
                    avg_time_unit = each_data.avg_time_unit
                    lat = each_data.lat
                    lon = each_data.lon

                    arr_data = np.array(
                        [time, value, unit, avg_time, avg_time_unit, lat, lon],
                        dtype=dtype,
                    ).reshape(1, 7)

                    grp = each_data.location + "/" + each_data.parameter
                    if grp in f:
                        f[grp].resize((f[grp].shape[0] + 1), axis=0)
                        f[grp][-1:] = arr_data
                    else:
                        f.create_dataset(grp, data=arr_data, maxshape=(None, 7))


# #############################################

# The functions here-in also works but aren't the most efficient ones.
# They might require large memory or space.
# Use with caution
# Or the functions are redundant without major improvement

# ##############################################

# def read_openaq_year(data_path, year):

#     """
#     The function is not advisable due to the time it can take,
#     though is working without a bug.
#     """

#     daily_list = _generate_daily_list(year)
#     print("Overriding daily list. The following line should be commented")
#     print("The year now has only 3 random days for testing")

#     daily_list = ["2018-01-01", "2018-06-05", "2018-07-18"]

#     data = []
#     for each_day in daily_list:
#         day_path = data_path + each_day
#         data.extend(read_opeaq_day(day_path))
#         print(f"Read the data for {each_day}")

#     return data


# def _unzip_concat(path):
#     """
#     This command creates a concatenated unzipped file and does not delete any file.
#     Remember always to delete the files after use.
#     Run _del_json
#     """

#     day = path[-11:-1]
#     unzip_cmd = "gzip -k -d " + path + "*.gz"
#     os.system(unzip_cmd)
#     # Add a newline after each EOF
#     concatenate_cmd = 'for f in ' + path + '*.ndjson; do (cat "${f}"; echo) >> '+ path + day + '.ndjson; done'
#     os.system(concatenate_cmd)


# def _del_ndjson(path):
#     """
#     Must be run after _unzip_concat
#     """

#     del_ndjson_cmd = "rm " + path + "*.ndjson"
#     os.system(del_ndjson_cmd)


# def read_openaq_day(path):
#     #  This functions speeds up the process by 1 or two seconds
#     strt_time = time.time()
#     # Clear ndjson if already present.
#     # Appending can increase file size exponentially.
#     # TO DO if the file exists don't run it, else run it.

#     _del_ndjson(path)
#     _unzip_concat(path)
#     day = path[-11:-1]

#     ndjson_filename = path + day + ".ndjson"

#     with open(ndjson_filename, 'r') as f:
#         data = []
#         for each_line in f:
#             single_dict = json.loads(each_line)
#             try:
#                 oaq = OpenaqData(single_dict)
#             except KeyError:
#                 oaq = OpenaqData(NO_DATA_DICT)
#             finally:
#                 data.append(oaq)

#     _del_ndjson(path)
#     print(f"The time take to read one day is {time.time()-strt_time}")

#     return data
