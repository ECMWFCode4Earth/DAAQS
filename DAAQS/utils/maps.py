import cartopy.crs as ccrs
import matplotlib.pylab as plt
import numpy as np
from matplotlib import cm


class ParameterMaps(object):
    def __init__(
        self,
        loc_lat_lon: set,
        parameter: str,
        year: int,
        month: int,
        w_path: str,
        degree=1,
    ):
        self.loc_lat_lon = loc_lat_lon
        self.parameter = parameter
        self.year = year
        self.month = str(month).zfill(2)
        self.w_path = w_path
        self.degree = degree
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
            f"Stations in each grid for {self.parameter} | year {self.year} | month {self.month}"
        )
        plt.colorbar(color_bar, fraction=0.023, pad=0.04)
        fname = (
            "coverage_"
            + self.parameter
            + "_"
            + str(self.year)
            + "_"
            + str(self.month)
            + ".png"
        )
        plt.savefig(self.w_path + str(self.year) + "/" + self.month + "/" + fname)

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
