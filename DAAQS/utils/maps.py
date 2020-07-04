import cartopy.crs as ccrs
import matplotlib.pylab as plt
import numpy as np
from matplotlib import cm
from DAAQS.utils.misc import generate_daily_list

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
        self.loc_lat_lon = self._read_lll_month()
        _lat, _lon, _z = self._generate_grid(degree=degree)
        self._lat = _lat
        self._lon = _lon
        self._z = _z

        self._generate_map()

    def _generate_map(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.coastlines()
        cmap = cm.get_cmap("Spectral", 5)
        color_bar = ax.pcolormesh(self._lon, self._lat, self._z, cmap=cmap)

        ax.set_title(
            f"Stations in each grid for {self.parameter} | year {self.year} | month {self.str_month}"
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
        plt.savefig("plots/coverage/" + fname)

    def _generate_grid(self, degree):

        loc_lat_lon = self.loc_lat_lon
        dx = self.degree
        dy = -self.degree
        _lat, _lon = np.mgrid[slice(90, -90 + dy, dy), slice(-180, 180 + dx, dx)]

        _z = np.NaN * np.ones_like(_lat)[:-1, :-1]

        for each in loc_lat_lon:
            index_lon = int((each[2] + 180) / dx)
            index_lat = int((each[1] - 90) / dy)

            if np.isnan(_z[index_lat, index_lon]):
                _z[index_lat, index_lon] = 1
            else:
                _z[index_lat, index_lon] += 1

        return _lat, _lon, _z

    def _read_lll_day(self, day ):
        f_path = "data/processed/lll_openaq/" + day + "/lll_"+day+"_"+self.parameter+".csv"
        with open(f_path, "r") as f:
            
            # Get rid of header
            f.readline()

            lll_set = set()
            for each_line in f:
                
                # Use reverse technique
                try:
                    lon , lat, loc = each_line[::-1].split(",",2)
                    lll_set.add((loc[::-1],float(lat[::-1]),float(lon[::-1])))
                except:
                    print(each_line[::-1].split(",",3))
                    

        return lll_set

    def _read_lll_month(self):
        daily_list = generate_daily_list(self.year, month = self.month)
        lll_set = set()
        for each_day in daily_list:
            lll_set = lll_set.union(self._read_lll_day(each_day[:-1]))
        return lll_set