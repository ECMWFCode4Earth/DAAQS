from DAAQS import w_gzip, w_lll


# local path

root_path = "/Users/mohit/Documents/DAAQS/data/"
data_path = "openaq/"
day = "2018-01-01/"
w_path = root_path + "processed/openaq/"
r_path = root_path + data_path
# # fname = "1514765764.ndjson.gz"



# ec2 path

# root_path = "/home/esowc24/"
# data_path = "data/openaq/"
# day = "2018-01-01/"
# r_path = root_path + data_path
# w_p


for year in [2018, 2019]:
    for month in range(1, 13):
        parameter = "pm10"
        w_gzip(r_path, w_path, year, month)
        #w_lll(r_path, w_path, year, parameter, month)
