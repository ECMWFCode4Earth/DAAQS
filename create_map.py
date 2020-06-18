from DAAQS import r_lll
from DAAQS import ParameterMaps

# local path

root_path = "/Users/mohit/Documents/DAAQS/data/"
data_path = "openaq/"
day = "2018-01-01/"
path = root_path + "processed/openaq/"
#  fname = "1514765764.ndjson.gz"



# ec2 path

# root_path = "/home/esowc24/"
# data_path = "data/openaq/"
# day = "2018-01-01/"
# r_path = root_path + data_path
# w_p

year = 2018
parameter = "pm10"
month = 1

lll_set, dist_arr = r_lll(r_path=path, year=2018, parameter="pm10", month=1)

ParameterMaps(lll_set, parameter, year, month, w_path=path)