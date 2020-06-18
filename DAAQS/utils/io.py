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


def _generate_daily_list(year, **kwargs):

    strt_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    if "month" in kwargs.keys():
        month = kwargs["month"]
        strt_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1)

    num_days = end_date - strt_date

    daily_list = []
    for day in range(num_days.days):
        dt = strt_date + timedelta(days=day)
        dt_str = dt.strftime("%Y-%m-%d")
        daily_list.append(dt_str + "/")

    return daily_list


def loc_lat_lon(path, year, parameter, month):
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

    # daily_list = _generate_daily_list(year)
    daily_list = _generate_daily_list(year, month=month)
    month = str(month).zfill(2)
    # Comment Later
    print("Overriding daily list. The following line should be commented")
    print("The year has 3 random days for testing")
    daily_list = ["2018-01-01/", "2018-06-05/", "2018-07-18/"]

    loc_lat_lon = set()
    data_dist = []

    for each in tqdm(daily_list):
        daily_path = path + each
        data = read_openaq_day(daily_path)
        counter = 0
        for each in data:
            if each.location == "None":
                counter += 1

            if parameter == "all":
                loc_lat_lon.add((each.location, each.lat, each.lon))

            elif each.parameter == parameter:
                loc_lat_lon.add((each.location, each.lat, each.lon))

        # print(f"The number of unused datapoints are {counter}")
        # print(f"The total number of datapoints are {len(data)}")
        data_dist.append((counter, len(data)))

    return loc_lat_lon, data_dist


def w_lll(r_path, w_path, year, parameter, month=1):

    lll, dist = loc_lat_lon(r_path, year, parameter, month=month)
    month = str(month).zfill(2)
    lll_path = w_path + "lll_" + str(year) + "_" + month + "_" + parameter + ".csv"
    with open(lll_path, "w") as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["loc", "lat", "lon"])
        for row in lll:
            csv_out.writerow(row)

    lll_path = w_path + "dist_" + str(year) + "_" + month + ".csv"
    with open(lll_path, "w") as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["removed", "total"])
        for row in dist:
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


def w_h5py(data_path, write_path, year: int, month=1):

    daily_list = _generate_daily_list(year, month=month)
    month = str(month).zfill(2)

    print("Overriding daily list. The following line should be commented")
    print("The year now has only 3 random days for testing")

    daily_list = ["2018-01-01/", "2018-06-05/", "2018-07-18/"]

    #  Initialising with a none type data

    # with h5py.File(write_path, "w") as f:
    #     data = OpenaqData(NO_DATA_DICT)
    #     grp = data.location + "/" + data.parameter

    #     time = data.time.strftime("%Y/%M/%d %H:%M:%S")
    #     value = data.value
    #     unit = data.unit
    #     avg_time = data.avg_time
    #     avg_time_unit = data.avg_time_unit
    #     lat = data.lat
    #     lon = data.lon

    #     dtype = h5py.special_dtype(vlen=str)

    #     arr_data = np.array(
    #         [time, value, unit, avg_time, avg_time_unit, lat, lon], dtype=dtype
    #     ).reshape(1, 7)

    #     f.create_dataset(grp, data=arr_data, maxshape=(None, 7))

    for each_day in tqdm(daily_list):
        day_path = data_path + each_day
        data = read_openaq_day(day_path)

        dtype = h5py.special_dtype(vlen=str)

        for each_data in data:

            if each_data.location != "None":
                time = each_data.time.strftime("%Y/%M/%d %H:%M:%S")
                value = each_data.value
                unit = each_data.unit
                avg_time = each_data.avg_time
                avg_time_unit = each_data.avg_time_unit
                lat = each_data.lat
                lon = each_data.lon

                arr_data = np.array(
                    [time, value, unit, avg_time, avg_time_unit, lat, lon], dtype=dtype,
                ).reshape(1, 7)

                loc = each_data.location.replace("/", "_slash_")
                d_path = write_path + str(year) + "/" + month + "/"

                if not os.path.isdir(d_path):
                    os.mkdir(d_path)
                f_name = loc + ".h5"
                w_path = d_path + f_name
                with h5py.File(w_path, "a") as f:
                    grp = each_data.parameter
                    if grp in f:
                        f[grp].resize((f[grp].shape[0] + 1), axis=0)
                        f[grp][-1:] = arr_data
                    else:
                        f.create_dataset(grp, data=arr_data, maxshape=(None, 7))


# def _read_h5py(path, parameter):
#     with h5py.File(path, "r") as f:
#         data =f[parameter][:,:]
#         return data


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
