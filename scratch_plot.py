from DAAQS import outlier_station_plot

center  = [28.6, 77.20]
lat_lon_class = [[28.3, 77.4 , 1],[28.8, 77.0, 0] ,[28.8, 77.4, -1] ]


outlier_station_plot(center, lat_lon_class, factor=10)