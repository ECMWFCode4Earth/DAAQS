from DAAQS import Statistics

region_list = ["India", "Europe", "Global"]
parameter_list = ["pm25", "so2", "no2", "o3"]
comp_with_list = ["cams", "openaq"]

region =  "Europe"
parameter = "pm25"
comp_with = "cams"

for region in region_list:
    for parameter in parameter_list:
        for comp_with in comp_with_list:
            x = Statistics(parameter)
            x.regional_plot(method = "COPOD", region=region, comp_with=comp_with)
            x.regional_plot(method = "KNN", region=region, comp_with=comp_with)
            x.regional_plot(method = "PCA", region=region, comp_with=comp_with)
            print(x.stats)
