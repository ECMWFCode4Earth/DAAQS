from DAAQS import read_openaq_day, _read_cams
from datetime import datetime
import numpy as np

data_path = "data/raw/openaq/"
day = "2019-01-01/"

day_path = data_path + day 

data_AQ = read_openaq_day(day_path)

# AQ_time = datetime.strptime(data_AQ[0].time, "%Y-%m-%dT%H:%M:%S.%fZ")

print (data_AQ[0].value, data_AQ[0].time, data_AQ[0].location, data_AQ[0].parameter, data_AQ[0].lat, data_AQ[0].lon)


data_CAM = _read_cams(day[:-1], "pm25")

dt = datetime.strptime(day[:-1], "%Y-%m-%d")

str_date = datetime(1900,1,1)

current_hour = (dt - str_date)
print (current_hour*24)

dict_sub = {}

for data in data_AQ:
    index_lat, index_lon= int((90 - data.lat)/0.75),  - int(data.lon/0.75)

    if data.lat >= - 90 and data.lon >=0:
        mean_dataCAM = np.mean(data_CAM['pm2p5'][:,index_lat,index_lon])
    

    mean_sub = (mean_dataCAM - data.value)

    key_name = str(index_lat) + '_' + str(index_lon)

    if key_name in dict_sub:
        dict_sub[key_name].append(mean_sub)

    else:
        dict_sub[key_name] = [mean_sub]

dict_mean = {}

for key, value in dict_sub.items():

    dict_mean[key] = np.mean(value)

    




# print(data_CAM['latitude'][:], data_CAM['longitude'][:], )

