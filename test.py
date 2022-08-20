from datetime import datetime
from datetime import timedelta
from datetime import timezone
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)

week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
year = beijing_now.timetuple().tm_year
month = beijing_now.timetuple().tm_mon
day = beijing_now.timetuple().tm_mday
today = datetime.date(datetime(year=year, month=month, day=day))
week = week_list[today.isoweekday() % 7]

print(year,month,day,today,week)
