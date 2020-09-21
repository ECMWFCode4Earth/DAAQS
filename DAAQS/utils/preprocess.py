import numpy as np

from DAAQS.utils.misc import index_to_center

def temporal_average(c_data, o_data, index_lat, index_lon):

    ## Ideally CAMS data is time_step x 3 x 3
    ## And openaq_data is list of all stations in that 3x3 grid 

    ## CAMS Data
    c_grid = c_data[:,index_lat-1:index_lat+2,index_lon-1:index_lon+2]

    cams_list = [[] for k in range(8)]

    for time in range(c_grid.shape[0]):
        index_time = time%8
        cams_list[index_time].append(np.ravel(c_grid[time,:,:]))
    cams_stack = np.stack(cams_list)
    cams_avg = np.mean(cams_stack, axis = 1)
    
    c_dict = dict()

    lat_0, lon_0 = index_to_center(index_lat-1,index_lon-1)
    lat_1, lon_1 = index_to_center(index_lat,index_lon) 
    lat_2, lon_2 = index_to_center(index_lat+1,index_lon+1) 

    coordinate_list = [(lat_0, lon_0), (lat_0, lon_1), (lat_0, lon_2), 
                       (lat_1, lon_0), (lat_1, lon_1), (lat_1, lon_2), 
                       (lat_2, lon_0), (lat_2, lon_1), (lat_2, lon_2),]

    for grid in range(cams_avg.shape[1]):    
        if "grid_"+str(grid) in c_dict:
            pass
        else: 
            c_dict["grid_"+str(grid)] = list(cams_avg[:,grid])
            c_dict["grid_"+str(grid)].append({"coordinates":coordinate_list[grid]})
    # cams_avg is 8x9 values which is at each 9 location we have 1x8 different values 

    ## OPENAQ Data
    
    o_dict = dict()
    for lat in range(index_lat-1,index_lat+2):
        for lon in range(index_lon-1, index_lon+2):
            for time in range(len(o_data)):
                for obs in o_data[time][lat][lon]:
                    time_index = time%8
                    if obs.location in o_dict:
                        o_dict[obs.location][time_index].append(obs.value)
                    else:
                        o_dict[obs.location] = [[],[],[],[],[],[],[],[], {"coordinates":(obs.lat, obs.lon)}]

    for each in o_dict:
        for i in range(8):
            try:
                vals = o_dict[each][i]
                o_dict[each][i] = sum(vals)/len(vals)
            except:
                o_dict[each][i] = -1
    
    return c_dict, o_dict 