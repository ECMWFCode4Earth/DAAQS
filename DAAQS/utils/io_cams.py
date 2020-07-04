from netCDF4 import Dataset

from DAAQS.utils.constants import cams_dict


def _read_cams(day, parameter):
    fname = cams_dict[parameter] + "_" + day + ".nc"
    fdir = "./DAAQS/data/cams/"
    fpath = fdir + fname
    data = Dataset(fpath, "r")

    return data


# class CAMS_Data(object):
#     def __init__(self, data):
#         self.data = data

#     def _get
