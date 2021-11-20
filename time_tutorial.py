import datetime

x = datetime.datetime.now()
now99 = datetime.datetime.now()
now1 = now99.strftime("%H:%M:%S")

time_1 = datetime.timedelta(hours=0, minutes=0, seconds=0)

s1 = now99.strftime("%H:%M:%S")
s2 = '09:00:00'
FMT = '%H:%M:%S'
tdelta = datetime.datetime.strptime(s1, FMT) - datetime.datetime.strptime(s2, FMT)
print(tdelta.total_seconds())
print(tdelta > time_1)

print(now99)
