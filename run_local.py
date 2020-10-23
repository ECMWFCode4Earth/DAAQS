from DAAQS import CAMSData, OpenAQData
from DAAQS import temporal_average, Model
from DAAQS import LocalPlot
from DAAQS import lat_lon_index, generate_day_list
from tqdm import tqdm

import time 

strt_time  = time.time()
day = "2019-10-25"
span = 3
parameter = "pm25"
comp_with = "cams"

location = "Leipzig"
lat = 51.34
lon = 12.37

# loc_name = "London"
# lat = 51.50
# lon = 0.12

# loc_name = "Zurich"
# lat = 47.37
# lon = 8.541

# loc_name = "Beijing"
# lat = 39.90
# lon = 116.407

# loc_name = 'Delhi'
# lat = 28.70
# lon = 77.10 

# loc_name = "blank"

# lat = 10
# lon = 10

# location = "SF"
# lat = 38.0
# lon = -122.419

# loc_name = "Good"
# lat = 49.0
# lon = 2.25

# loc_name = "Bad"
# lat = 51.0
# lon = 4.5

# loc_name = "Mixed"
# lat = 51.0
# lon = 3.0



lat_index, lon_index = lat_lon_index((lat, lon))

c_data = CAMSData(day, span, parameter).data

o_data = OpenAQData(day, span, parameter).data
c_dict, o_dict = temporal_average(c_data,o_data, lat_index, lon_index)

model = Model(c_dict, o_dict)
A_C, B_C, C_C = model.pred_COPOD(comp_with=comp_with)
A_K, B_K, C_K = model.pred_KNN(comp_with=comp_with)
A_P, B_P, C_P = model.pred_PCA(comp_with=comp_with)

plot_dir = "plots/local/"

l_plot_C = LocalPlot(c_dict, o_dict, A_C, B_C, C_C, 
                    parameter = parameter, day =day, span = span, method= "COPOD", 
                    plot_dir = plot_dir, loc_name= loc_name, comp_with = comp_with)

l_plot_K = LocalPlot(c_dict, o_dict, A_K, B_K, C_K, 
                    parameter = parameter, day =day, span = span, method= "KNN", 
                    plot_dir = plot_dir, loc_name= loc_name, comp_with = comp_with)

l_plot_P = LocalPlot(c_dict, o_dict, A_P, B_P, C_P, 
                    parameter = parameter, day =day, span = span, method= "PCA", 
                    plot_dir = plot_dir, loc_name= loc_name, comp_with = comp_with)

l_plot_C.class_ts_plot()
l_plot_C.class_spatial_plot()

l_plot_K.class_ts_plot()
l_plot_K.class_spatial_plot()

l_plot_P.class_ts_plot()
l_plot_P.class_spatial_plot()