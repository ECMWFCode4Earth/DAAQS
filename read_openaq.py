from DAAQS import w_lll, read_openaq_day


# local path

# root_path = "/Users/mohit/Documents/DAAQS/data/"
# data_path = "openaq/"
# day = "2018-01-01/"
# w_path = root_path + "processed/openaq/"
# r_path = root_path + data_path
# # # fname = "1514765764.ndjson.gz"



# ec2 path

data_path = "data/raw/openaq/"
day = "2018-01-01/"

day_path = data_path + day

data = read_openaq_day(day_path)

print (data[0].value, data[0].time, data[0].location, data[0].parameter, data[0].lat, data[0].lon)