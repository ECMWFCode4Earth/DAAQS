from DAAQS import CAMSMaxPlot, OpenAQMaxPlot, MaxDiffPlot
from tqdm import tqdm
parameter = "no2"
day_list = ["2019-01-01", "2019-02-01", "2019-03-01", 
       "2019-04-01", "2019-05-01", "2019-06-01", 
       "2019-07-01", "2019-08-01", "2019-09-01", 
       "2019-10-01", "2019-11-01", "2019-12-01"]

for day in tqdm(day_list):
    CAMSMaxPlot(parameter, day = day)
    #OpenAQMaxPlot(parameter, day = day)
    #MaxDiffPlot(parameter, day = day)