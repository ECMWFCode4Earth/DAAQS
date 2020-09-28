from netCDF4 import Dataset
from DAAQS.utils.constants import cams_fname_dict, oaq_cams_dict
from datetime import datetime, timedelta
import numpy as np

class CAMSData(object):
    
    def __init__(self, day, span, parameter):
        self.day = day
        self.dt = datetime.strptime(self.day, "%Y-%m-%d")
        self.span = span
        self.parameter = parameter
        

        if self.span == 0:
            self.dt_list = [self.dt]
        elif span > 0 :
            self.dt_list  = [self.dt + timedelta(days = delta) for delta in range(-self.span,self.span+1)]
        else : 
            assert span >= 0 ,"Span is not non-negative integer"

        self.data = self._read_cams()
        
    def _read_cams(self):
        list_data = []
        for each_day in self.dt_list:
            str_day = datetime.strftime(each_day, "%Y-%m-%d")
            fname = cams_fname_dict[self.parameter] + "_" + str_day + ".nc"
            fdir = "data/raw/cams/"
            fpath = fdir + fname

            # We convert while reading the data only
            conversion_factor = 1
            if self.parameter == "pm25":
                # pm25 in ug/m3
                conversion_factor = 1.0e9
            elif self.parameter == "so2":
                conversion_factor = 1
            elif self.parameter == "no2":
                conversion_factor == 1
            elif self.parameter == "o3":
                conversion_factor = 1

            

            daily_data = Dataset(fpath, "r")[oaq_cams_dict[self.parameter]][:,:,:]
            daily_data[daily_data<1e-9] = 0
            daily_data = daily_data*conversion_factor
            
            list_data.append(daily_data)

        return np.vstack(list_data)