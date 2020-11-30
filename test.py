import datetime

today = datetime.date.today()
month_ago = today - datetime.timedelta(days=30)
str_today = today.strftime("%Y-%m-%d")
str_month_ago = month_ago.strftime("%Y-%m-%d")
print(type(str_today), str_today, str_month_ago)