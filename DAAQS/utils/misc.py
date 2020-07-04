from datetime import datetime, timedelta

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