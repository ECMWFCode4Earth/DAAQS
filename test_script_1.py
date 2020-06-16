from DAAQS import loc_lat_lon
from DAAQS import ParameterMaps
from DAAQS import write_h5py, read_openaq_day, loc_lat_lon

root_path = "/home/esowc24/"
data_path = "data/openaq/"
day = "2018-01-01/"
# fname = "1514765764.ndjson.gz"

# path = root_path+data_path
# loc_lat_lon = loc_lat_lon(path, 2018, "pm10")

# loc = set()
# for each in loc_lat_lon:
#     loc.add(each[0])

# print(len(loc))


path = root_path + data_path
write_path = root_path+"DAAQS_data/processed/openaq/"


# loc_lat_lon = loc_lat_lon(path, 2018, "pm10")

# ParameterMaps(loc_lat_lon)

write_h5py(path, write_path, 2018)

