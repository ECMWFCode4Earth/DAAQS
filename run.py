from DAAQS import CAMSData, OpenAQData, temporal_average, Model, StationsMap, generate_day_list
from tqdm import tqdm

import time 

strt_time  = time.time()
day = "2019-01-04"
span = 0
parameter =  "pm25"
comp_with = "openaq"
n_steps = 20

day_list= generate_day_list(day, step_size=2*span+1, n_steps=n_steps)

t_A_KNN = []
t_B_KNN = []
t_C_KNN = []

for day in day_list:

    c_data = CAMSData(day, span, parameter).data

    o_data = OpenAQData(day, span, parameter).data

    ## We know that lat ranges from 0, 240 and lon ranges from 0, 479
    s_A_KNN = []
    s_B_KNN = []
    s_C_KNN = []

    for index_lat in tqdm(range(1,240)):
        for index_lon in range(1,479):
            c_dict, o_dict = temporal_average(c_data,o_data, index_lat, index_lon )
            model = Model(c_dict, o_dict)
            A_loc_KNN, B_loc_KNN, C_loc_KNN = model.pred_KNN(k=5, comp_with = comp_with)
            s_A_KNN.extend(A_loc_KNN)
            s_B_KNN.extend(B_loc_KNN)
            s_C_KNN.extend(C_loc_KNN)
    
    t_A_KNN.append(s_A_KNN)
    t_B_KNN.append(s_B_KNN)
    t_C_KNN.append(s_C_KNN)

outlier_maps = StationsMap(t_A_KNN,t_B_KNN, t_C_KNN)

outlier_maps.generate_overall_plot("plots/knn_5_20.png", "outputs/knn_5_20.csv")


print(f"The total time taken by the script is {time.time()-strt_time:.3f}")