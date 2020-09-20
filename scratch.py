from DAAQS import CAMSData, OpenAQData, temporal_average

day = "2019-01-04"
span = 3

parameter =  "pm25"

c_data = CAMSData(day, span, parameter).data

o_data = OpenAQData(day, span, parameter).data

index_lat = 82
index_lon = 103


c_dict, o_dict = temporal_average(c_data,o_data, index_lat, index_lon )

print(c_dict)
print(o_dict)