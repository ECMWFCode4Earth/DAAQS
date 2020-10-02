from datetime import datetime, timedelta
import numpy as np


def generate_day_list(day, step_size=7, n_steps = 52):
    strt_dt = datetime.strptime(day, "%Y-%m-%d")

    dt_list = []
    for i in range(n_steps):
        dt_list.append(strt_dt)
        strt_dt += timedelta(days=step_size)

    return [datetime.strftime(dt, "%Y-%m-%d") for dt in dt_list]

def generate_daily_list(year, **kwargs):

    strt_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    if "month" in kwargs.keys():
        month = kwargs["month"]
        if month == 12:
            strt_date = datetime(year, month, 1)
            end_date = datetime(year + 1, 1, 1)
        else:
            strt_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1)

    num_days = end_date - strt_date

    daily_list = []
    for day in range(num_days.days):
        dt = strt_date + timedelta(days=day)
        dt_str = dt.strftime("%Y-%m-%d")
        daily_list.append(dt_str + "/")

    return daily_list

def gen_radial_coordinates(time):
    theta = 2*np.pi*time/24
    x1 = np.cos(theta)
    x2 = np.sin(theta)

    return x1,x2

def index_to_center(index_lat, index_lon):
    grid_size = 0.75
    lat = 90-grid_size*index_lat
    lon =  grid_size*index_lon
    return lat, lon

def lon_transform_0_base(lon):
    if lon <0:
        lon = lon+360
    return lon

def lon_transform_minus180_base(lon):
    if lon >180:
        lon = lon-360
    return lon

def lat_lon_index(lat_lon):
    lat = lat_lon[0]
    lon = lat_lon[1]
    