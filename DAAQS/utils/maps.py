import cartopy.crs as ccrs
import matplotlib.pylab as plt
import numpy as np
from matplotlib import cm
from DAAQS.utils.misc import generate_daily_list
from DAAQS.utils.io_cams import CAMSData
from DAAQS.utils.io_openaq import OpenAQData
from DAAQS.utils.constants import oaq_cams_dict
from DAAQS.utils.analysis import max_openaq_grid, max_cams_grid

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
