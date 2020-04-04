from datetime import *
from datetime import timedelta

DATE_UPDATE = str(date.today().strftime('%m-%d-%Y'))
DATE_PREV_UPDATE = str((date.today() - timedelta(days = 1)).strftime('%m-%d-%Y'))
#DATE_UPDATE = DATE_PREV_UPDATE

start = datetime(2020, 1, 22)
end = datetime.today()
step = timedelta(days=7)

time_list = []
while start < end:
    time_list.append(str(start.strftime('%m-%d-%Y')))
    start += step

if DATE_UPDATE not in time_list:
    time_list.append(DATE_UPDATE)
