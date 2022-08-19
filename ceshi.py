# -*- coding: utf-8 -*-
import http.client
import json  # 引入json库
import urllib

conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
params = urllib.parse.urlencode({'key': '填入你的key'})
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn.request('POST', '/lzmy/index', params, headers)
res = conn.getresponse()
data = res.read()
data = json.loads(data)  # 转换成字典
data = data.get("newslist", "未找到值")[0]
data = data.get("saying", "未找到值")
print(data)

# 模板
# 今天是{{date.DATA}}
# {{city.DATA}} {{weather.DATA}} 当前{{real.DATA}} 今日{{min_temperature.DATA}}-{{max_temperature.DATA}} 降雨概率{{pop.DATA}}%
# {{wind.DATA}}，风力{{windsc.DATA}}，湿度{{humidity.DATA}}%，紫外线指数{{uvindex.DATA}}。
# {{tips.DATA}}
#
# 我们已经认识{{meet_day.DATA}}天啦！
# 今天是我们恋爱的第{{love_day.DATA}}天哦！
# 距离宝贝生日还有{{birthday1.DATA}}天~
# 距离我的生日还有{{birthday2.DATA}}天~
#
# {{lizhi.DATA}}
#
# {{note_en.DATA}}
# {{note_ch.DATA}}
#
# {{pipi.DATA}}
