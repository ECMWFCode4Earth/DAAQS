import cartopy.crs as ccrs
import matplotlib.pylab as plt
import numpy as np
from matplotlib import cm
import cartopy.io.img_tiles as cimgt
from shapely.geometry.polygon import LinearRing

from DAAQS.utils.misc import generate_daily_list, lon_transform_0_base, lon_transform_minus180_base
from DAAQS.utils.io_cams import CAMSData
from DAAQS.utils.io_openaq import OpenAQData
from DAAQS.utils.constants import oaq_cams_dict
from DAAQS.utils.analysis import max_openaq_grid, max_cams_grid

import time

class ParameterMaps(object):
    def __init__(
        self,
        parameter: str,
        year: int,
        month: int,
        degree=0.75,
    ):
        self.parameter = parameter
        self.year = year
        self.month = month
        self.str_month = str(self.month).zfill(2)
        self.degree = degree
        self.lat_lon = self._read_ll_month()
        _z, _lat, _lon = self._generate_grid(degree=degree)
        self._lat = _lat
        self._lon = _lon
        self._z = _z
        self.vmax = 6
        self._generate_map()

    def _generate_map(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.coastlines()
        cmap = cm.get_cmap("Spectral", 5)
        color_bar = ax.pcolormesh(self._lon, self._lat, self._z, cmap=cmap, vmax = self.vmax)

        ax.set_title(
            f"Stations per grid for {self.parameter} in {self.str_month}, {self.year}"
        )
        plt.colorbar(color_bar, fraction=0.023, pad=0.04)
        fname = (
            "coverage_"
            + self.parameter
            + "_"
            + str(self.year)
            + "_"
            + self.str_month
            + ".png"
        )
        fig.tight_layout()
        plt.savefig("plots/coverage/" + fname)
        plt.close()

    def _generate_grid(self, degree):

        lat_lon = self.lat_lon
        dx = self.degree
        dy = self.degree
        _lat, _lon = np.mgrid[slice(90, -90 - dy, -dy), slice(-180, 180 + dx, dx)]

        _z = np.NaN * np.ones_like(_lat)[:-1, :-1]

        for each in lat_lon:
            index_lon = int((each[1]+180) / dx)
            index_lat = int((90-each[0]) / dy)
    
            if np.isnan(_z[index_lat, index_lon]):
                _z[index_lat, index_lon] = 1
            else:
                
                _z[index_lat, index_lon] += 1
        return _z, _lat, _lon

    def _read_ll_day(self, day ):
        f_path = "data/processed/ll_openaq/" + day + "/ll_"+day+"_"+self.parameter+".csv"
        with open(f_path, "r") as f:
            
            # Get rid of header
            f.readline()

            ll_set = set()
            for each_line in f:
                try:
                    lat, lon = each_line.split(",")
                    ll_set.add((float(lat),float(lon)))
                except:
                    print(f"Exception in lat and lon {each_line}")
                    
        return ll_set

    def _read_ll_month(self):
        daily_list = generate_daily_list(self.year, month = self.month)
        ll_set = set()
        for each_day in daily_list:
            ll_set = ll_set.union(self._read_ll_day(each_day[:-1]))
        return ll_set

class CAMSMaxPlot(object):
    def __init__(self, parameter, day):
        z, lat, lon = max_cams_grid(parameter, day)
        self.parameter = parameter
        self.day = day
        self.z = z
        self.lat = lat
        self.lon = lon 
        self.vmax = 3000
        self.unit = "UNK"
        if self.parameter == "pm25":
            self.unit = "$\mu$g/$m^3$"
        self._generate_map()
         

    def _generate_map(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.coastlines()
        cmap = cm.get_cmap("OrRd")
        color_bar = ax.pcolormesh(self.lon, self.lat, self.z, cmap=cmap, vmin=0, vmax = self.vmax)
        
        ax.set_title(
            f"Maximum {self.parameter} on {self.day} in {self.unit}"
        )
        plt.colorbar(color_bar, fraction=0.023, pad=0.04)
        fname = (
            "cams_max_"
            + self.parameter
            + "_"
            + str(self.day)
            + ".png"
        )
        fig.tight_layout()
        plt.savefig("plots/cams/" + fname)
        plt.close()

class OpenAQMaxPlot(object):
    def __init__(self, parameter, day):
        z, lat, lon = max_openaq_grid(parameter, day)
        self.parameter = parameter
        self.day = day
        self.z = z
        self.lat = lat
        self.lon = lon 
        self.vmax = 3000
        self.unit = "UNK"
        if self.parameter == "pm25":
            self.unit = "$\mu$g/$m^3$"
        self._generate_map()
        

    def _generate_map(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.coastlines()
        cmap = cm.get_cmap("OrRd")
        color_bar = ax.pcolormesh(self.lon, self.lat, self.z, cmap=cmap, vmin = 0, vmax = self.vmax)

        ax.set_title(
            f"Maximum {self.parameter} on {self.day} in {self.unit}"
        )
        plt.colorbar(color_bar, fraction=0.023, pad=0.04 )
        fname = (
            "openaq_max_"
            + self.parameter
            + "_"
            + str(self.day)
            + ".png"
        )
        fig.tight_layout()
        plt.savefig("plots/openaq/" + fname)
        plt.close()

class MaxDiffPlot(object):
    def __init__(self, parameter, day):
        z_oaq, lat_oaq, lon_oaq = max_openaq_grid(parameter, day)
        z_cams, lat_cams, lon_cams = max_cams_grid(parameter, day)
        self.parameter = parameter
        self.day = day
        self.z = z_oaq - z_cams
        self.lat = lat_oaq
        self.lon = lon_oaq 
        self._generate_map()

    def _generate_map(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.coastlines()
        cmap = cm.get_cmap("OrRd")
        color_bar = ax.pcolormesh(self.lon, self.lat, self.z)

        ax.set_title(
            f"Max Diff plot for {self.parameter} on {self.day}"
        )
        plt.colorbar(color_bar, fraction=0.023, pad=0.04)
        fname = (
            "max_diff"
            + self.parameter
            + "_"
            + str(self.day)
            + ".png"
        )
        plt.savefig("plots/difference/" + fname)
        plt.close()


def outlier_station_plot(center, lat_lon_class, factor = 8, fpath = "plots/outlier_plot.png"):

    delta = 0.75
    square_lons = [77.20-delta,77.20-delta,77.20+delta,77.20+delta]
    square_lats = [28.6-delta,28.6+delta,28.6+delta,28.6-delta]

    stamen_terrain = cimgt.Stamen('terrain-background')

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(projection=stamen_terrain.crs)
    ax.set_extent([77.20+factor*delta, 77.20-factor*delta,28.6-factor*delta,28.6+factor*delta  ] , ccrs.PlateCarree())
    ax.add_image(stamen_terrain, 8)
    ax.plot(center[1], center[0], marker='o', color='k', markersize=6,
                alpha=0.7, transform=ccrs.Geodetic())
    ring = LinearRing(list(zip(square_lons, square_lats)))
    ax.add_geometries([ring], ccrs.PlateCarree(), facecolor='none', edgecolor='black')

    for i in range(len(lat_lon_class)):
        if lat_lon_class[i][2] == 1 :
            color = "r"
        elif lat_lon_class[i][2] == 0:
            color = "g"
        elif lat_lon_class[i][2] == -1:
            color = "grey"

        ax.plot(lat_lon_class[i][1], lat_lon_class[i][0], marker='o', color=color, markersize=4,
                alpha=0.7, transform=ccrs.Geodetic())

    ax.gridlines(crs=ccrs.PlateCarree(), draw_labels = True)
    plt.savefig(fpath)

class StationsMap(object):
    def __init__(self,A_station, B_station, C_station):
        self.list_A_station = A_station
        self.list_B_station = B_station
        self.list_C_station = C_station

        # We are using a 4 color color pallete

        self.c1 = "#ff6d69" # light_red
        self.c2 = "#fecc50" # light_yellow
        self.c3 = "#0be7fb" # light_blue
        self.c4 = "#010b8b" # dark blue
        self.c5 = "#1e0521" # blackish        

        self.s = 0.5

    def generate_step_plot(self, map_name, file_name,  step = 1):

        A_station = self.list_A_station[step-1]
        B_station = self.list_B_station[step-1]
        C_station = self.list_C_station[step-1]
        

        fig = plt.figure(figsize=(12,8), dpi = 240)
        
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        
        A_lat, A_lon = self._generate_list_lat_lon(A_station)
        B_lat, B_lon = self._generate_list_lat_lon(B_station)
        C_lat, C_lon = self._generate_list_lat_lon(C_station)

        ax.scatter(C_lon, C_lat, color = self.c5, s = self.s)
        ax.scatter(B_lon, B_lat, color = self.c4, s = self.s)
        ax.scatter(A_lon, A_lat, color = self.c1, s = self.s)

        ax.coastlines()
        
        ax.stock_img()
        ax.gridlines(crs=ccrs.PlateCarree(), draw_labels = True)
        plt.savefig(map_name)

    def generate_overall_plot(self, map_name, file_name):

        combined_dict = dict()
        for A_station in self.list_A_station:
            for A in A_station:
                if A[1] in combined_dict:
                    combined_dict[A[1]][1]+=1
                else:
                    combined_dict[A[1]] = [A[0], 1, 0, 0]

        for B_station in self.list_B_station:
            for B in B_station:
                if B[1] in combined_dict:
                    combined_dict[B[1]][2]+=1
                else:
                    combined_dict[B[1]] = [B[0], 0, 1, 0]

        for C_station in self.list_C_station:
            for C in C_station:
                if C[1] in combined_dict:
                    combined_dict[C[1]][3]+=1
                else:
                    combined_dict[C[1]] = [C[0], 0, 0, 1]
        
        self.combined_dict = combined_dict
        self._write_files(file_name, combined_dict)
        
        fig = plt.figure(figsize=(12,8), dpi = 240)
        ax = fig.add_subplot(projection=ccrs.PlateCarree())

        lon_list = []
        lat_list = []
        z_list = []

        for key, value in combined_dict.items():
            lat = key[0]
            lon = key[1]

            z = value[1]+value[3]/(value[1]+value[2]+value[3])

            combined_dict[key].append(z)

            if z >0:
                if value[0].split("_")[0] != "grid":
                    lon = lon_transform_minus180_base(lon)
                    lon_list.append(lon)
                    lat_list.append(lat)
                    z_list.append(z)

        ax.scatter(lon_list, lat_list, c = z_list, s = self.s,  cmap = "Spectral", alpha = 0.6)
        
        self.combined_dict = combined_dict
        ax.coastlines()
        ax.stock_img()
        ax.gridlines(crs=ccrs.PlateCarree(), draw_labels = True)
        plt.savefig(map_name)
    
    def _write_files(self, file_name, loc_dict):
        with open(file_name, "w") as f:
            f.write("lat,lon,count_A,count_B,count_C,location\n")
            for key,val in loc_dict.items():
                f.write(str(key[0])+","+str(key[1])+","+str(val[1])+","+str(val[2])+","+str(val[3])+","+val[0]+"\n")

    def _generate_list_lat_lon(self, station, cams=False):
        list_lat = []
        list_lon = []
        
        for s in station:
            lat, lon = s[1]
            
            if s[0].split("_")[0]== "grid":
                if cams == False:
                    pass
                else:
                    lon = lon_transform_minus180_base(lon)
                    list_lat.append(lat)
                    list_lon.append(lon)

            else:
                list_lat.append(lat)
                list_lon.append(lon)

        return list_lat, list_lon

class LocalPlot(object):
    def __init__(self,c_dict, o_dict, A_location, B_location, C_location, **kwargs) :
        self.c_dict = c_dict
        self.o_dict = o_dict
        self.A_location = A_location
        self.B_location = B_location
        self.C_location = C_location
        self.unit = "[UNK]"
        self.parameter = "UNK"
        self.day = "UNK"
        self.span = "UNK"
        self.param_name = "UNK"
        self.method="UNK"
        self.plot_dir = "/"
        self.prefix = ""
        self.loc_name = "UNK"


        if "parameter" in kwargs:
            self.parameter = kwargs["parameter"]
        if "day" in kwargs:
            self.day = kwargs["day"]
        if "span" in kwargs:
            self.span = kwargs["span"]
        if "method" in kwargs:
            self.method = kwargs["method"]
        if "plot_dir" in kwargs:
            self.plot_dir = kwargs["plot_dir"]
        if "prefix" in kwargs:
            self.prefix = kwargs["prefix"]
        if "loc_name" in kwargs:
            self.loc_name = kwargs["loc_name"]
        if "comp_with" in kwargs:
            self.comp_with = kwargs["comp_with"]

        if self.parameter == "pm25":
            self.param_name = "PM2.5"
            self.unit = "[ug/m3]"
        elif self.parameter == "so2":
            self.param_name = "SO2"
            self.unit = "[ppm]"
        elif self.parameter == "no2":
            self.param_name = "NO2"
            self.unit = "[ppm]"
        elif self.parameter == "o3":
            self.param_name = "O3"
            self.unit = "[ppm]"
        
        # We are using a 4 color color pallete

        self.c1 = "#ff6d69" # light_red
        self.c2 = '#ffbe4f' # "#fecc50"  light_yellow
        self.c3 = "#0be7fb" # light_blue
        self.c4 = "#010b8b" # dark blue
        self.c5 = "#1e0521" # blackish       

        # Grid Size

        self.grid_size = 0.75
        self.marker_size = 2
        self.centre = self.c_dict["grid_4"][8]["coordinates"]

    def class_spatial_plot(self):
        
        factor = 1.1
        delta = 3/2*self.grid_size*factor
        
        stamen_terrain = cimgt.Stamen('terrain-background')

        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(projection=stamen_terrain.crs)
        ax.set_extent([self.centre[1]+delta, self.centre[1]-delta,self.centre[0]-delta,self.centre[0]+delta] 
                        , ccrs.PlateCarree())
        ax.add_image(stamen_terrain, 8)

        for A in self.A_location:
            ax.plot(A[1][1], A[1][0], marker='o', color=self.c1, markersize=self.marker_size,
                alpha=1.0, transform=ccrs.Geodetic())
        
        for B in self.B_location:
            ax.plot(B[1][1], B[1][0], marker='o', color=self.c4, markersize=self.marker_size,
                alpha=1.0, transform=ccrs.Geodetic())
        
        for C in self.C_location:
            ax.plot(C[1][1], C[1][0], marker='o', color=self.c5, markersize=self.marker_size,
                alpha=1.0, transform=ccrs.Geodetic())
        
        ring_list = [self._gen_ring(self.c_dict["grid_"+str(i)][8]["coordinates"]) for i in range(9)]

        ax.add_geometries(ring_list, ccrs.PlateCarree(), facecolor='none', edgecolor='black')

        ax.gridlines(crs=ccrs.PlateCarree(), draw_labels = True)
        map_name = "_".join([self.prefix,"spatial", self.method, self.parameter, self.comp_with, self.loc_name, self.day, str(self.span)])
        map_name = self.plot_dir+map_name+".png"
        plt.savefig(map_name)

    def class_ts_plot(self):
        cams_data = []
        for _, val in self.c_dict.items():
            cams_data.append(val[:8])
        
        A_data = []
        B_data = []
        C_data = []

        for _, val in self.o_dict.items():
            for A_loc in self.A_location:
                if val[8]["coordinates"] == A_loc[1]:
                    A_data.append(val[:8])
            for B_loc in self.B_location:
                if val[8]["coordinates"] == B_loc[1]:
                    B_data.append(val[:8])

            for C_loc in self.C_location:
                if val[8]["coordinates"] == C_loc[1]:
                    C_data.append(val[:8])

        cams_arr = self._stack(cams_data)       
        A_arr = self._stack(A_data)
        B_arr = self._stack(B_data)
        C_arr = self._stack(C_data)

        ylabel = " ".join(self.param_name + self.unit)
        xlabel = "Hour of the day"
        title = "Avg time series | Span : " + str(self.span) + " | Day :  " + self.day + "\n" \
                + "Parameter : " +self.parameter + "| Method : " + self.method
        fig, ax = plt.subplots(1,1, figsize=(6,4), dpi = 240)
        
        #cams_ax = ax.plot(cams_arr, color = self.c2, linestyle = "dashdot", label = "CAMS Data")
        c_ax = ax.plot(C_arr, color = self.c5, linestyle = "dashdot")
        b_ax = ax.plot(B_arr, color = self.c4, linestyle = "dashdot", label = "Type B OpenAQ station")
        #a_ax = ax.plot(A_arr, color = self.c1, linestyle = "dashdot", label = "Type A OpenAQ station")
        ax.set_xticklabels(["", "0-3","3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-24"])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(bottom = -1e-3)
        ax.set_title(title)
        #ax.legend(handles=[cams_ax[0], b_ax[0], a_ax[0]], loc='best')
        map_name = "_".join([self.prefix,"ts", self.method, self.parameter, self.comp_with, self.loc_name, self.day, str(self.span)])
        map_name = self.plot_dir+map_name+".png"
        plt.savefig(map_name)

    def _stack(self,list_data):
        if list_data == []:
            return []
        else:
            return np.stack(list_data).T

    def _gen_ring(self, centre):
        
        lat, lon = centre

        lon = lon_transform_minus180_base(lon)
        
        delta = self.grid_size/2.0
        square_lons = [lon-delta,lon-delta,lon+delta,lon+delta]
        square_lats = [lat-delta,lat+delta,lat+delta,lat-delta]
        ring = LinearRing(list(zip(square_lons, square_lats)))

        return ring