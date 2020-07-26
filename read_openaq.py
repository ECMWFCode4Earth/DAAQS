from DAAQS import OpenAQData

day = "2018-01-02"

openaq = OpenAQData(day, span = 1)

openaq.sort_dict()

for each in openaq.data_dict["Pahala"]:
    if each.parameter == "pm25":
        print(each.value)
        print(each.time)