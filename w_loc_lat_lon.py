from DAAQS import loc_lat_lon
import csv


# local path
# root_path = "/Users/mohit/Documents/DAAQS/data/"
# data_path = "openaq/"
# day = "2018-01-01/"
# fname = "1514765764.ndjson.gz"

# ec2 path

root_path = "/home/esowc24/"
data_path = "data/openaq/"
day = "2018-01-01/"

path = root_path+data_path
loc_lat_lon = loc_lat_lon(path, 2018, "pm10")

with open(path + "loc_lat_lon/lll_2018_pm10.csv", 'w') as f:
    csv_out = csv.writer(f)
    csv_out.writerow(["loc", "lat", "lon"])
    for row in loc_lat_lon:
        csv_out.writerow(row)
