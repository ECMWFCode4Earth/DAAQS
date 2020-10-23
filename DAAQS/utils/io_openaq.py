import csv
import gzip
import json
import os
from datetime import datetime, timedelta
import operator
import h5py
import numpy as np
from tqdm import tqdm

from DAAQS.utils.constants import MAX_ATTR_DICT, OAQ_UNIT_DICT, OAQ_CONV_FACTOR 
from DAAQS.utils.cfg import openaq_folder

class OpenAQData(object):
    def __init__(self, day, span, parameter):    
        self.day = day
        self.dt = datetime.strptime(self.day, "%Y-%m-%d")
        self.span = span
        self.parameter = parameter
        self.tot_data_points = 0
        self.good_data_points = 0
        self.grid_size = 0.75
        
        if self.span == 0:
            self.dt_list = [self.dt]
        elif span > 0 :
            self.dt_list  = [self.dt + timedelta(days = delta) for delta in range(-self.span,self.span+1)]
        else : 
            assert span >= 0 ,"Span is not non-negative integer"
        
        list_data = self._read_openaq()
        self.ungridded_data = []
        for each in list_data:
            self.ungridded_data.extend(each)
        self.data = self._gridded_data()


    def _read_openaq_day(self, day):
        str_day = datetime.strftime(day, "%Y-%m-%d")
        path = openaq_folder + str_day + "/" 
        file_list = [x for x in os.listdir(path) if x.split(".")[-1] == "gz"]
        data = []
        for each in file_list:
            fpath = path + each
            data.extend(self._read_gzip_file(fpath))
        # print(f"The time taken to read one day is {time.time()-strt_time}")
        return data

    def _read_openaq(self):
        list_data = []
        for each_day in self.dt_list:
            list_data.append(self._read_openaq_day(each_day))

        return list_data

    def _read_gzip_file(self, path):
        
        with gzip.GzipFile(path, "r") as jsonzip:
            data = []

            for each_json in jsonzip:
                single_dict = json.loads(each_json)

                try:
                    oaq = OAQ(single_dict)
                except KeyError:
                    oaq = OAQ(MAX_ATTR_DICT)
                finally:
                    self.tot_data_points+=1
                    if oaq.parameter == self.parameter:
                        self.good_data_points+=1
                        if oaq.unit != OAQ_UNIT_DICT[self.parameter]:
                            try:
                                oaq.value = oaq.value*OAQ_CONV_FACTOR[oaq.parameter][oaq.unit]
                                oaq.unit = "ppm"
                                data.append(oaq)                        
                            except :
                                print(f"Cannot recognise the unit {oaq.unit} for parameter {self.parameter}")
                        else:
                            data.append(oaq)                        
        return data

    def _gridded_data(self):

        start_date = self.dt - timedelta(days=self.span)

        time_dim = (2*self.span+1)*8
        data = [[[[] for k in range(480)] for j in range(241)] for i in range(time_dim)]
        for obs in self.ungridded_data:
            hours_from_start  = (obs.time - start_date).seconds/(60*60) 
            ## Convert longitude 
            if obs.lon<0:
                lon  = 360+obs.lon
            else:
                lon = obs.lon

            index_time = int(hours_from_start/3)
            index_lat = int((90+self.grid_size/2.0-obs.lat)/self.grid_size)
            
            if lon > 360-self.grid_size/2:
                index_lon = 0
            else:
                index_lon = int((lon+self.grid_size/2.0)/self.grid_size)
            
            if index_time >=0:    
                data[index_time][index_lat][index_lon].append(obs)
        
        return data

    def _sort_location(self):
        self.ungridded_data.sort(key=operator.attrgetter("location"))

    def sort_dict(self):
        _data_dict = dict()
        self._sort_location()
        for each in self.ungridded_data:
            if each.location in _data_dict:
                _data_dict[each.location].append(each)
            else:
                _data_dict[each.location] = [each]
        self.data_dict = _data_dict


def _generate_daily_list(year, **kwargs):

    strt_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    if "month" in kwargs.keys():
        month = kwargs["month"]
        if month == 12:
            strt_date = datetime(year, month, 1)
            end_date = datetime(year + 1, 1, 1)
        else:
            strt_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1)

    num_days = end_date - strt_date

    daily_list = []
    for day in range(num_days.days):
        dt = strt_date + timedelta(days=day)
        dt_str = dt.strftime("%Y-%m-%d")
        daily_list.append(dt_str + "/")

    return daily_list


def lat_lon(year, parameter, month):
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
    # print("Overriding daily list. The following line should be commented")
    # print("The year has 3 random days for testing")
    # daily_list = ["2018-01-01/", "2018-06-05/", "2018-07-18/"]

    lat_lon = set()
    data_dist = []
    ll_list = []

    for each in tqdm(daily_list):
        daily_path = "data/raw/openaq/" + each
        data = read_openaq_day(daily_path)
        counter = 0
        for each in data:
            if each.location == "None":
                counter += 1

            if parameter == "all":
                lat_lon.add((each.lat, each.lon))

            elif each.parameter == parameter:
                lat_lon.add((each.lat, each.lon))

        # print(f"The number of unused datapoints are {counter}")
        # print(f"The total number of datapoints are {len(data)}")
        data_dist.append((counter, len(data)))
        ll_list.append(lat_lon)

    return ll_list, data_dist, daily_list


def w_ll(year, parameter, month=1):

    ll, dist, daily_list = lat_lon(year, parameter, month=month)
    for i in range(len(daily_list)):
        each_day = daily_list[i]
        directory = "data/processed/ll_openaq/" + str(each_day)
        _make_dir(directory)

        ll_fname = "ll_" + str(each_day[:-1]) + "_" + parameter + ".csv"

        ll_path = directory + ll_fname

        with open(ll_path, "w") as f:
            csv_out = csv.writer(f)
            csv_out.writerow(["lat", "lon"])
            for row in ll[i]:
                csv_out.writerow(row)

        dist_fname = "dist_" + str(each_day[:-1]) + ".csv"

        dist_path = directory + dist_fname

        with open(dist_path, "w") as f:
            csv_out = csv.writer(f)
            csv_out.writerow(["removed", "total"])
            csv_out.writerow(dist[i])


class OAQ(object):
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
        "j_hour"
    )

    def __init__(self, json_dict):
        """
        Standardised storage for data.
        Time is always stored  in 'UTC'
        Standard units are as follows:

        PM10 = ug/m3
        Ozone =
        SO2 =
        averaging time is in hours
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
        self.j_hour = self._julian_hour()

    def _julian_hour(self):
        strt_date = datetime(1900,1,1)
        julian_hour = (self.time - strt_date)
        return julian_hour



def _make_dir(path):

    if not os.path.exists(path):
        os.mkdir(path)


