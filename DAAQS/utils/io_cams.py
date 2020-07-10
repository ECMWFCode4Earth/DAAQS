from netCDF4 import Dataset
from DAAQS.utils.constants import cams_fname_dict
from datetime import datetime, timedelta


class CAMSData(object):
    
    def __init__(self, parameter, day, span):
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
            list_data.append(Dataset(fpath, "r"))
        
        return list_data