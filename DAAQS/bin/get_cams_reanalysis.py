import datetime
import tempfile
from shutil import copyfile

import cdo
import cdsapi
import yaml

"""
create an ADS account at https://ads.atmosphere.copernicus.eu
and load ADS credentials.
"""

with open("/Users/mohit/.cdsapirc", "r") as f:
    credentials = yaml.safe_load(f)

c = cdsapi.Client(url=credentials["url"], key=credentials["key"])


# The directory to store data, A data folder with a sub directory as CAMS_data is created.
# data is also added to the gitignore file.

DATADIR = "data/CAMS_data"


variables = [
    # "surface_pressure",
    # "temperature",
    # "carbon_monoxide",
    # "nitrogen_dioxide",
    # "ozone",
    "particulate_matter_10um",
    # "particulate_matter_2.5um",
    # "sulphur_dioxide",
]
to_convert = ["carbon_monoxide", "nitrogen_dioxide", "ozone", "sulphur_dioxide"]
R = 287.058

start = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
date_generated = [
    start + datetime.timedelta(days=x) for x in range(0, (end - start).days)
]

dates = []
for date in date_generated:
    dates.append(date.strftime("%Y-%m-%d"))


cdo = cdo.Cdo()

for dataDate in dates:

    for variable in variables:

        c.retrieve(
            "cams-global-reanalysis-eac4",
            {
                "variable": variable,
                "date": dataDate,
                "time": [
                    "00:00",
                    "03:00",
                    "06:00",
                    "09:00",
                    "12:00",
                    "15:00",
                    "18:00",
                    "21:00",
                ],
                "format": "netcdf",
                "model_level": "60",
            },
            "{}/{}_{}.nc".format(DATADIR, variable, dataDate),
        )

        if variable in to_convert:
            with tempfile.NamedTemporaryFile() as f1, tempfile.NamedTemporaryFile() as f2:
                sp = "{}/surface_pressure_{}.nc".format(DATADIR, dataDate)
                t = "{}/temperature_{}.nc".format(DATADIR, dataDate)
                varin = "{}/{}_{}.nc".format(DATADIR, variable, dataDate)
                varout = "{}/{}_{}.nc".format(DATADIR, variable, dataDate)

                # unpack data
                for aa in [sp, t, varin]:
                    print(aa, f1.name)
                    cdo.copy(input=aa, output=f1.name, options="-b f32")
                    copyfile(f1.name, aa)

                # compute mass concentration from mass mixing ratio
                cdo.mul(input=" ".join((varin, sp)), output=f1.name)
                cdo.div(input=" ".join((f1.name, t)), output=f2.name)
                cdo.divc(R, input=f2.name, output=varout)
