from DAAQS import CAMSData, OpenAQData, temporal_average, Model, OutlierMaps, generate_day_list
from tqdm import tqdm

import time 


strt_time  = time.time()
day = "2019-01-03"
span = 0
parameter =  "pm25"

c_data = CAMSData(day, span, parameter).data

o_data = OpenAQData(day, span, parameter).data

## We know that lat ranges from 0, 240 and lon ranges from 0, 479

index_lat = 8
index_lon = 2

c_dict, o_dict = temporal_average(c_data,o_data, index_lat, index_lon )
print(c_dict)
print(o_dict)
model = Model(c_dict, o_dict)

pred_KNN = model.pred_KNN(k = 5)
print(pred_KNN)
outlier_loc_KNN, other_loc_KNN = model.pred_location(pred_KNN)