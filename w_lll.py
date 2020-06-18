from DAAQS import loc_lat_lon, write_lll
import csv


# local pat
root_path = "/Users/mohit/Documents/DAAQS/data/"
data_path = "openaq/"
day = "2018-01-01/"
fname = "1514765764.ndjson.gz"


# ec2 path

# root_path = "/home/esowc24/"
# data_path = "data/openaq/"
# day = "2018-01-01/"

path = root_path+data_path
year = 2018
parameter = "o3"

write_lll(path, year, parameter)
