from DAAQS import CAMSData, OpenAQData, temporal_average, Model, StationsMap, generate_day_list
from tqdm import tqdm

import time 

strt_time  = time.time()
day = "2019-01-03"
span = 0
parameter =  "so2"

day_list= generate_day_list(day, step_size=2*span+1, n_steps=1)

t_A_KNN = []
t_B_KNN = []
t_C_KNN = []

for day in day_list:

    c_data = CAMSData(day, span, parameter).data
    
    o_data = OpenAQData(day, span, parameter).data
    
    # We know that lat ranges from 0, 240 and lon ranges from 0, 479
    s_A_KNN = []
    s_B_KNN = []
    s_C_KNN = []

    c_dict, o_dict = temporal_average(c_data,o_data, 82, 103)


    model = Model(c_dict, o_dict)

    A_loc_KNN, B_loc_KNN, C_loc_KNN = model.pred_KNN(k = 3, comp_with= "cams")

    s_A_KNN.extend(A_loc_KNN)
    s_B_KNN.extend(B_loc_KNN)
    s_C_KNN.extend(C_loc_KNN)

    t_A_KNN.append(s_A_KNN)
    t_B_KNN.append(s_B_KNN)
    t_C_KNN.append(s_C_KNN)

outlier_maps = StationsMap(t_A_KNN,t_B_KNN, t_C_KNN)

# #outlier_maps.generate_overall_plot("overall.png")
outlier_maps.generate_step_plot("check.png")

# print(f"The total time taken by the script is {time.time()-strt_time:.3f}")