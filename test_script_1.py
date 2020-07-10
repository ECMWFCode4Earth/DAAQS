from DAAQS import lat_lon

ll_list,_,_ = lat_lon(2019, "no2", 1)
print(ll_list[:100])