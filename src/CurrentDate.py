from datetime import date
from datetime import timedelta

DATE_UPDATE = str(date.today().strftime('%m-%d-%Y'))
DATE_PREV_UPDATE = str((date.today() - timedelta(days = 1)).strftime('%m-%d-%Y'))
