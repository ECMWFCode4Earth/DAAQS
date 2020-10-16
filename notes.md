### Reading the data

- All that is needed to run and get the plot is the script ```run.py```
- There are two classes to read the cams and the open aq data seperately
- 'CAMSData(day, span, parameter)' and OPENAQData(day, span, parameter)
-  Both requires the day value, the span value and the parameter value. Span describes number of days around the day values. For examples a span of 3 days means data for 7 days in total, i.e a week
- parameter is the species for example pm25
- .data attribute of CAMS data gives a 3D array while for OpenAQ data it gives 4D list. Array can be indexed as X[time, lat, lon], 4 D list can be indexed as X[time][lat][lon]. For Open AQ the X[time][lat][lon] this gives a list of all data points present in the particular cams grid in particular time interval
- Fuurther Model class is used for prediction 
- For KNN the time taken to run this model is roughly 600 (591.299) seconds for 1 month of 1 species 
- Thus for 1 year for each species it should roughly take 2 hours. Which is manageable under current approach

### Some infomration about the Unit

##### Cpnversion Factor

| Species | CAMS | OpenAQ |
|PM2.5| kg/m3 | ug/m3
|NO2| kg/kg | ppm & ug/m3
|SO2| kg/kg | ppm & ug/m3
|O3| kg/kg | ppm & ug/m3

PM2.5 in CAMS is in kg/m3 while in openAQ is ug/m3 - 1e9

nohup python run.py &> comp_with_cams_pm25.txt &