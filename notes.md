### Reading the data

- All that is needed to run and get the plot is the script rum.py
- There are two classes to read the cams and the open aq data seperately
- 'CAMSData(day, span, parameter)' and OPENAQData(day, span, parameter)
-  Both requires the day value, the span value and the parameter value. span describes number of days around the day values. For examples a span of 3 days means data for 7 days in total, i.e a week
- parameter is the species for example pm25
- .data attribute of CAMS data gives a 3D array while for OpenAQ data it gives 4D list. Array can be indexed as X[time, lat, lon], 4 D list can be indexed as X[time][lat][lon]. For Open AQ the X[time][lat][lon] this gives a list of all data points present in the particular cams grid in particular time interval
- Fuurther Model class is used for prediction 