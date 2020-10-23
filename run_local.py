from DAAQS import CAMSData, OpenAQData
from DAAQS import temporal_average, Model
from DAAQS import LocalPlot
from DAAQS import lat_lon_index

day = "2019-10-25"
span = 3
parameter = "pm25"
comp_with = "cams"

#  Define the location 
loc_name = 'Delhi'
lat = 28.70
lon = 77.10 

# Find the index of of cams grid for a particular lat and lon
lat_index, lon_index = lat_lon_index((lat, lon))

# Read CAMS and OPENAQ data
c_data = CAMSData(day, span, parameter).data
o_data = OpenAQData(day, span, parameter).data

# Temporally avearage the data
c_dict, o_dict = temporal_average(c_data,o_data, lat_index, lon_index)

# Initilause the model with the avaerage data
model = Model(c_dict, o_dict)

# Make predictions using different method
A_C, B_C, C_C = model.pred_COPOD(comp_with=comp_with)
A_K, B_K, C_K = model.pred_KNN(comp_with=comp_with)
A_P, B_P, C_P = model.pred_PCA(comp_with=comp_with)

# Chose a plot directory
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