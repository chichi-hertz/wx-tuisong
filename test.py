# -*- coding: utf-8 -*-
import http.client, urllib
import json
conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
params = urllib.parse.urlencode({'key':'ff69b7cb0b0eba39e8660ea5adfec1c2','city':'平湖'})
headers = {'Content-type':'application/x-www-form-urlencoded'}
conn.request('POST','/tianqi/index',params,headers)
res = conn.getresponse()
data = res.read()
data = json.loads(data)
data = data.get("newslist")[0]
# 地区
# area = data.get("area")
# # 天气
# weather = data.get("weather")
# # 最高温
# highest = data.get("highest")
# # 最低温
# lowest = data.get("lowest")
# # 降雨概率
# pop = data.get("pop")
# print(area,weather,highest,lowest,pop)
print(data)