from DAAQS.utils.io_cams import CAMSData
from DAAQS.utils.io_openaq import OpenAQData
from DAAQS.utils.constants import oaq_cams_dict
import numpy as np


def max_openaq_grid(parameter,day):
    openaq_data = OpenAQData(day=day, span=0)
    
    day_data = openaq_data.data[0]
    
    dx = 0.75
    dy = 0.75
    _lat, _lon = np.mgrid[slice(90, -90 - dy, -dy), slice(0, 360+ dx, dx)]
    _z = np.NaN * np.ones_like(_lat)[:-1, :-1]
    for each_data in day_data:
        if each_data.lat!= -9999 and each_data.lon!= -9999:

            index_lat, index_lon= int((90 - each_data.lat)/0.75),   int(each_data.lon/0.75)
            if np.isnan(_z[index_lat, index_lon]):
                _z[index_lat, index_lon] = each_data.value
            else: 
                _z[index_lat, index_lon] = max(_z[index_lat, index_lon], each_data.value)
    return _z, _lat, _lon
    
def max_cams_grid(parameter, day):
    cams_data = CAMSData(parameter = parameter, day=day, span=0)
    data = cams_data.data[0]
    print(data[oaq_cams_dict[parameter]])
    factor = 1
    if parameter == "pm25":
        factor = 10e9    
    _z = np.max(data[oaq_cams_dict[parameter]][:,:,:], axis = 0)[:-1, :]*factor

    dx = dy = 0.75

    _lat, _lon = np.mgrid[slice(90, -90 - dy, - dy), slice(0, 360+ dx, dx)]

    return _z, _lat, _lon
