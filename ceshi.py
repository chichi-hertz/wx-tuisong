# -*- coding: utf-8 -*-
import http.client
import json  # 引入json库
import urllib
import http.client
import json
import os
import random
import sys
import urllib
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from time import time

import requests
from requests import get, post

import cityinfo
# conn = http.client.HTTPSConnection('http://timor.tech/api/holiday/info/')  # 接口域名
# # params = urllib.parse.urlencode({'key': '填入你的key'})
# headers = {'Content-type': 'application/x-www-form-urlencoded'}
# conn.request('GET', 'SweetNothings')
# res = conn.getresponse()
# data = res.read()
# # data = json.loads(data)  # 转换成字典
# # data = data.get("newslist", "未找到值")[0]
# # data = data.get("saying", "未找到值")
from datetime import datetime

import requests

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
todatymd = today.strftime("%Y%m%d")
isWeekDay = requests.get(url='http://tool.bitefu.net/jiari/', params='d={}'.format(todatymd))
isWeekDay = isWeekDay.text
isWeekDay = json.loads(isWeekDay)
if isWeekDay == 1:
    weekTips='既然今天是休息日，那我的宝贝就可以多睡一会儿啦~'
elif isWeekDay == 2:
    weekTips='今天是小长假哦~宝贝能好好休息啦~'
else:
    if week == '星期一':
        weekTipsLib = ['周一周一 呆若木鸡',
                       '今天周一呜呜呜呜呜呜呜',
                       '人生很短 周一很长',
                       '周一奶茶一杯 一周快乐起飞'
                       ]
        weekTips = random.choice(weekTipsLib)
    if week == '星期二':
        weekTipsLib = ['周二摆烂 以烂制烂',
                       '周二划水 喝茶抖腿',
                       '周二摸鱼 心旷神怡',
                       '周二喝拿铁 遇事都能解'
                       ]
        weekTips = random.choice(weekTipsLib)
    if week == '星期三':
        weekTipsLib = ['熬过周三 翻过大山',
                       '周三周三 一座大山',
                       '周三瑞纳冰 心态更年轻'
                       ]
        weekTips = random.choice(weekTipsLib)
    if week == '星期四':
        weekTipsLib = ['周四不卷 卧倒消遣',
                       '周四躺平 量力而行',
                       '熬过星期四 世上无难事',
                       '周四加班崩溃 来杯葡萄冰萃',
                       '疯狂星期四，谁请我吃？'
                       ]
        weekTips = random.choice(weekTipsLib)
    if week == '星期五':
        weekTipsLib = ['周五没有文案 只有快乐',
                       '周五五五五五',
                       '熬过星期五 生龙又活虎',
                       '周五就该有周五的样子 有事下周再说',
                       '周五了 该摆烂了'
                       '周五领导检查 别慌点杯奶茶'
                       ]
        weekTips = random.choice(weekTipsLib)
print(weekTips)

# 模板
# 今天是{{date.DATA}}
# {{city.DATA}} {{weather.DATA}} 当前{{real.DATA}} 今日{{min_temperature.DATA}}-{{max_temperature.DATA}} 降雨量{{pcpn.DATA}}毫米
# {{wind.DATA}}，风力{{windsc.DATA}}，湿度{{humidity.DATA}}%，紫外线指数{{uvindex.DATA}}。
# {{weektips.DATA}}
# {{temptips.DATA}}{{raintips.DATA}}
#
# 我们已经认识{{meet_day.DATA}}天啦！
# 今天是我们恋爱的第{{love_day.DATA}}天哦！
# 距离宝贝生日还有{{birthday1.DATA}}天~
# 距离我的生日还有{{birthday2.DATA}}天~
#
# {{note_en.DATA}}
# {{note_ch.DATA}}
# {{lovetips.DATA}}
#
