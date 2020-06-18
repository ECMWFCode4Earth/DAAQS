from DAAQS import w_h5py, w_lll


# ocal path

root_path = "/Users/mohit/Documents/DAAQS/data/"
data_path = "openaq/"
day = "2018-01-01/"
w_path = root_path + data_path
r_path = root_path + data_path
# # fname = "1514765764.ndjson.gz"



# ec2 path

# root_path = "/home/esowc24/"
# data_path = "data/openaq/"
# day = "2018-01-01/"
# r_path = root_path + data_path
# w_path = root_path+"DAAQS_data/processed/openaq/"

year = 2018
month = 1
parameter = "pm10"
w_h5py(r_path, w_path, year, month)
w_lll(r_path, w_path, year, parameter, month)
