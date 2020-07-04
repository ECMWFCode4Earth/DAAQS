from DAAQS import _read_cams

data = _read_cams("2019-01-01", "pm25")

print(data["time"])