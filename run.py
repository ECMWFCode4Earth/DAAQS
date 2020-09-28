from DAAQS import CAMSData, OpenAQData, temporal_average, Model, OutlierMaps, generate_day_list
from tqdm import tqdm

import time 

strt_time  = time.time()
day = "2019-01-04"
span = 3
parameter =  "pm25"

day_list= generate_day_list(day, step_size=2*span+1, n_steps=52)

t_outlier_KNN = []
t_other_KNN = []

for day in day_list:

    c_data = CAMSData(day, span, parameter).data

    o_data = OpenAQData(day, span, parameter).data

    ## We know that lat ranges from 0, 240 and lon ranges from 0, 479
    s_outlier_KNN = []
    s_other_KNN = []

    for index_lat in tqdm(range(1,240,3)):
        for index_lon in range(1,481,3):
            c_dict, o_dict = temporal_average(c_data,o_data, index_lat, index_lon )

            model = Model(c_dict, o_dict)

            pred_KNN = model.pred_KNN(k = 5)
            outlier_loc_KNN, other_loc_KNN = model.pred_location(pred_KNN)

            s_outlier_KNN.extend(outlier_loc_KNN)
            s_other_KNN.extend(other_loc_KNN)

    t_outlier_KNN.append(s_outlier_KNN)
    t_other_KNN.append(s_other_KNN)

outlier_maps = OutlierMaps(t_outlier_KNN,t_other_KNN)

outlier_maps.generate_overall_plot("overall.png")

print(f"The total time taken by the script is {time.time()-strt_time:.3f}")