MAX_ATTR_DICT = {
    "date": {"utc": "0001-01-01T00:00:00.000Z"},
    "parameter": "None",
    "location": "None",
    "value": -9999,
    "unit": "None",
    "averagingPeriod": {"unit": "None", "value": -9999},
    "coordinates": {"latitude": -9999, "longitude": -9999},
}

MIN_ATTR_DICT = {
    "date": {"utc": "0001-01-01T00:00:00.000Z"},
    "parameter": "None",
    "location": "None",
    "value": -9999,
    "coordinates": {"latitude": -9999, "longitude": -9999},
}

cams_fname_dict = {
    "pm10": "particulate_matter_10um",
    "pm25": "particulate_matter_2.5um",
    "o3": "ozone",
    "no2": "nitrogen_dioxide",
    "so2": "sulphur_dioxide"
}

oaq_cams_dict = {
    "pm25" : "pm2p5",
    "no2" : "no2",
    "so2" : "so2",
    "o3" : "go3"
}

oaq_unit_dict = {
    "pm25" : "µg/m³",
    "no2" : "ppm",
    "so2" : "ppm",
    "o3" : "ppm"
}