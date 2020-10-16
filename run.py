from DAAQS import CAMSData, OpenAQData, temporal_average, Model, StationsMap, generate_day_list
from tqdm import tqdm

import time 

strt_time  = time.time()
day = "2019-01-04"
span = 3
parameter =  "pm25"
comp_with_cams = "cams"
comp_with_openaq = "openaq"
n_steps = 52

day_list= generate_day_list(day, step_size=2*span+1, n_steps=n_steps)

t_A_KNN = []
t_B_KNN = []
t_C_KNN = []

t_A_PCA = []
t_B_PCA = []
t_C_PCA = []

t_A_COPOD = []
t_B_COPOD = []
t_C_COPOD = []

for day in day_list:

    c_data = CAMSData(day, span, parameter).data

    o_data = OpenAQData(day, span, parameter).data

    ## We know that lat ranges from 0, 240 and lon ranges from 0, 479
    s_A_KNN = []
    s_B_KNN = []
    s_C_KNN = []

    s_A_PCA = []
    s_B_PCA = []
    s_C_PCA = []

    s_A_COPOD = []
    s_B_COPOD = []
    s_C_COPOD = []

    for index_lat in tqdm(range(1,240)):
        for index_lon in range(1,479):
            c_dict, o_dict = temporal_average(c_data,o_data, index_lat, index_lon )
            model = Model(c_dict, o_dict)
            A_loc_KNN, B_loc_KNN, C_loc_KNN = model.pred_KNN(comp_with = comp_with_cams)
            s_A_KNN.extend(A_loc_KNN)
            s_B_KNN.extend(B_loc_KNN)
            s_C_KNN.extend(C_loc_KNN)
    
            A_loc_PCA, B_loc_PCA, C_loc_PCA = model.pred_PCA(comp_with = comp_with_cams)
            s_A_PCA.extend(A_loc_PCA)
            s_B_PCA.extend(B_loc_PCA)
            s_C_PCA.extend(C_loc_PCA)
            
            A_loc_COPOD, B_loc_COPOD, C_loc_COPOD = model.pred_COPOD(comp_with = comp_with_cams)
            s_A_COPOD.extend(A_loc_COPOD)
            s_B_COPOD.extend(B_loc_COPOD)
            s_C_COPOD.extend(C_loc_COPOD)
            
    t_A_KNN.append(s_A_KNN)
    t_B_KNN.append(s_B_KNN)
    t_C_KNN.append(s_C_KNN)

    t_A_PCA.append(s_A_PCA)
    t_B_PCA.append(s_B_PCA)
    t_C_PCA.append(s_C_PCA)

    t_A_COPOD.append(s_A_COPOD)
    t_B_COPOD.append(s_B_COPOD)
    t_C_COPOD.append(s_C_COPOD)

outlier_maps = StationsMap(t_A_KNN,t_B_KNN, t_C_KNN)
outlier_maps.generate_overall_plot("plots/overall_KNN_"+parameter+"_"+comp_with_cams+".png", "outputs/overall_KNN_"+parameter+"_"+comp_with_cams+".csv")

outlier_maps = StationsMap(t_A_PCA,t_B_PCA, t_C_PCA)
outlier_maps.generate_overall_plot("plots/overall_PCA_"+parameter+"_"+comp_with_cams+".png", "outputs/overall_PCA_"+parameter+"_"+comp_with_cams+".csv")

outlier_maps = StationsMap(t_A_COPOD,t_B_COPOD, t_C_COPOD)
outlier_maps.generate_overall_plot("plots/overall_COPOD_"+parameter+"_"+comp_with_cams+".png", "outputs/overall_COPOD_"+parameter+"_"+comp_with_cams+".csv")

print(f"The total time taken by the script is {time.time()-strt_time:.3f}")