from DAAQS import ParameterMaps

param_list = ["no2", "so2", "o3","pm25"]

# for year in [2018,2019]:
#     for month in range(1,13):
#         for param in param_list:
#             print(f"Creating maps for year {year} and month {month} for parameter {param}")
#             ParameterMaps(parameter = param, year = year, month = month)

ParameterMaps(parameter ="pm25", year = 2019, month = 7)