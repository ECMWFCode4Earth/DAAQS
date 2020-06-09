
from DAAQS import loc_lat_lon
from DAAQS import ParameterMaps

root_path = "/Users/mohit/Documents/DAAQS/data/"
data_path = "openaq/"
day = "2018-01-01/"
fname = "1514765764.ndjson.gz"

path = root_path + data_path

loc_lat_lon = loc_lat_lon(path,2018, "pm10")

ParameterMaps(loc_lat_lon)