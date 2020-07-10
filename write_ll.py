from DAAQS import w_ll


param_list = ["no2", "so2", "o3","pm25"]

for year in [2018, 2019]:
    for month in range(1,13):
        for param in param_list:
            print(f"Writing year {year} and month {month} for parameter {param}")
            w_ll(year, param, month)