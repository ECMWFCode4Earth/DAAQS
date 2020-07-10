from DAAQS import CAMSData, OpenAQData
from datetime import datetime
import numpy as np



parameter = "pm25"
day = "2019-02-01"

span = 0 # Very high span values can overload memory

cams_data = CAMSData(parameter = parameter, day=day, span=span )
openaq_data = OpenAQData(parameter = parameter, day=day, span=span )

print(cams_data.data[0])
print(openaq_data.data[0][0].value)







# dt = datetime.strptime(day[:-1], "%Y-%m-%d")

# str_date = datetime(1900,1,1)

# current_hour = (dt - str_date)
# print (current_hour*24)

# dict_sub = {}

# for data in data_AQ:
#     index_lat, index_lon= int((90 - data.lat)/0.75),  - int(data.lon/0.75)

#     if data.lat >= - 90 and data.lon >=0:
#         mean_dataCAM = np.mean(data_CAM['pm2p5'][:,index_lat,index_lon])
    

#     mean_sub = (mean_dataCAM - data.value)

#     key_name = str(index_lat) + '_' + str(index_lon)

#     if key_name in dict_sub:
#         dict_sub[key_name].append(mean_sub)

#     else:
#         dict_sub[key_name] = [mean_sub]

# dict_mean = {}

# for key, value in dict_sub.items():

#     dict_mean[key] = np.mean(value)

    




# # print(data_CAM['latitude'][:], data_CAM['longitude'][:], )

