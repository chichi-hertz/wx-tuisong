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


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    # print(random.choice(color_list))
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token


def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print('我是天气api请求的数据')
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn


def get_birthday(birthday, year, today):
    # 获取生日的月和日
    birthday_month = int(birthday.split("-")[1])
    birthday_day = int(birthday.split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


# 词霸每日一句
def get_ciba():
    if (Whether_Eng != "否"):
        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        note_en = r.json()["content"]
        note_ch = r.json()["note"]
        return note_ch, note_en
    else:
        return "", ""


# 彩虹屁
# def caihongpi():
#     if (caihongpi_API != "替换掉我"):
#         conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
#         params = urllib.parse.urlencode({'key': caihongpi_API})
#         headers = {'Content-type': 'application/x-www-form-urlencoded'}
#         conn.request('POST', '/caihongpi/index', params, headers)
#         res = conn.getresponse()
#         data = res.read()
#         data = json.loads(data)
#         data = data["newslist"][0]["content"]
#         if ('XXX' in data):
#             data = data.replace("XXX", "欣怡")
#         data = '「' + data + '」'
#         return data
#     else:
#         return ""


# 励志名言
# def lizhi():
#     if (lizhi_API != "替换掉我"):
#         conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
#         params = urllib.parse.urlencode({'key': lizhi_API})
#         headers = {'Content-type': 'application/x-www-form-urlencoded'}
#         conn.request('POST', '/lzmy/index', params, headers)
#         res = conn.getresponse()
#         data = res.read()
#         data = json.loads(data)
#         data = '「' + data["newslist"][0]["saying"] + '」'
#         return data
#     else:
#         return ""


# 下雨概率和建议
def tip():
    if (tianqi_API != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': tianqi_API, 'city': city})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/tianqi/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        print(data)
        # 天气
        weather = data["newslist"][0]["weather"]
        # 当前气温
        real = data["newslist"][0]["real"]
        # 最高气温
        temp = data["newslist"][0]["highest"]
        # 最低气温
        tempn = data["newslist"][0]["lowest"]
        # 降水概率
        pop = data["newslist"][0]["pop"]
        # 风向
        wind = data["newslist"][0]["wind"]
        # 风力
        windsc = data["newslist"][0]["windsc"]
        # 湿度
        humidity = data["newslist"][0]["humidity"]
        # 紫外等级
        uvindex = data["newslist"][0]["uv_index"]

        return weather, real, temp, tempn, pop, wind, windsc, humidity, uvindex
    else:
        return "", ""


# 推送信息
def send_message(to_user, access_token, city_name, weather, real, max_temperature, min_temperature, pop,
                 wind, windsc, humidity, uvindex, note_en, note_ch):
    temperatureTips = ''
    rainTips = ''
    loveTips = ''
    weekTips = ''
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
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
    # 获取休息日工作日API
    todatymd = today.strftime("%Y%m%d")
    isWeekDay = requests.get(url='http://www.ddung.org/jiari/', params='d={}'.format(todatymd))
    isWeekDay = isWeekDay.text
    isWeekDay = json.loads(isWeekDay)
    if isWeekDay == 1:
        weekTipsLib = ['既然今天是休息日，那我的宝贝就可以多睡一会儿啦~',
                       '宝贝休息日快乐！可以干点自己想干的事情啦~',
                       '休息日，吃饱饱！',
                       '今天是休息日啦啦啦啦啦啦啦啦',
                       '宝贝休息日快乐~有没有好好休息呀~'
                       ]
        weekTips = random.choice(weekTipsLib)
    elif isWeekDay == 2:
        weekTipsLib = ['既然今天是节假日，那我的宝贝就可以多睡一会儿啦~',
                       '今天是小长假哦~宝贝有没有好好休息呀~',
                       '今天是节假日啦啦啦啦啦啦啦啦'
                       ]
        weekTips = random.choice(weekTipsLib)
    elif isWeekDay == 0:
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
                           '周三瑞纳冰 心态更年轻',
                           'OMG周三困得想死'
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
        if week == '星期六':
            weekTipsLib = ['今天明明是周六...sad',
                           '累了！',
                           ]
            weekTips = random.choice(weekTipsLib)
        if week == '星期日':
            weekTipsLib = ['今天明明是周日...sad',
                           '调休人，调休魂，调休de都是人上人',
                           ]
            weekTips = random.choice(weekTipsLib)

    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取在一起的日子的日期格式
    meet_year = int(config["meet_date"].split("-")[0])
    meet_month = int(config["meet_date"].split("-")[1])
    meet_day = int(config["meet_date"].split("-")[2])
    meet_date = date(meet_year, meet_month, meet_day)
    # 获取在一起的日期差
    meet_days = str(today.__sub__(meet_date)).split(" ")[0]

    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    # 温度大于37度，触发热语句
    if int(max_temperature[:-1]) >= 37:
        temperatureTipsLib = ['今天好热呀宝贝！出门的话注意防暑防晒哦~',
                              '妈呀太热了今天！宝贝出门注意防暑呀~',
                              '热死啦热死啦热死啦！宝贝出门注意防暑防晒哦~',
                              '宝贝出门注意防暑防晒！要热化了呜呜呜...',
                              '热热热热热热热热热热热热热热热热...',
                              '非常燥热的一天...宝贝注意防暑！',
                              '热人闷人倦人的夏天...宝贝注意防暑！'
                              ]
        temperatureTips = random.choice(temperatureTipsLib)
    # 温度小于3度 触发冷语句
    if int(min_temperature[:-1]) <= 3:
        temperatureTipsLib = ['今天好冷呀宝贝！注意保暖注意保暖~',
                              '冻死我啦！宝贝注意保暖~',
                              '妈呀这个天也太冷了！宝贝注意保暖~',
                              '宝贝注意保暖！我的鼻涕被冻出来了呜呜呜...',
                              '冻得我木木的...宝贝注意保暖！',
                              '“不冷吗？”不冷才怪哦！宝贝注意保暖~',
                              '冷冷冷冷冷冷冷冷冷冷冻冻冻冻死我了'
                              ]
        temperatureTips = random.choice(temperatureTipsLib)
    # 降水概率大于70
    if int(pop) >= 65:
        rainTipsLib = ['最美的不是下雨天，是和你一起躲过雨的屋檐。',
                       '你笑时，雷声温柔，暴雨无声。',
                       '都怪雨下得那么急，都怪没有地方躲雨，才会一头撞进了你的怀里。',
                       '樱桃蒙上了薄薄的水雾，像绯红色的雨，我走在你的身后，满目皆暖。',
                       '我喜欢你，就像天气预报说，明天有雨我都能听成明天有你。',
                       '你不要淋到雨啦，不然你会可爱到发芽。',
                       '天气好时去见你，天气不好时带着伞去见你。',
                       '听雨的声音，一滴滴清晰，你的呼吸像雨滴渗入我的爱里。',
                       '你的爱是把大大的伞，给我最美的晴空。'
                       ]
        rainTips = random.choice(rainTipsLib)
    # 降水概率小于20
    elif int(pop) <= 25:
        rainTipsLib = ['心存阳光，必有诗和远方。',
                       '只要有你，我的每天都是晴天。',
                       '慢慢走，沿途有风景，背后有阳光。',
                       '远方是你，山川是你，蓝天白云是你，极致温柔是你。',
                       '晴天要快乐~',
                       '天气好得就像走着走着就能遇见你。',
                       '天气好时去见你，天气不好时带着伞去见你。'
                       ]
        rainTips = random.choice(rainTipsLib)
    # 特殊日子触发纪念日语句
    if int(love_days) % 100 == 0 | int(love_days) % 365 == 0:
        loveTips = '我们还会有很多很多个{}天。'.format(love_days)
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city": {
                "value": city_name,
                # "color": get_color()
            },
            "weather": {
                "value": weather,
                # "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature,
                "color": '#0e3ea9'
            },
            "max_temperature": {
                "value": max_temperature,
                "color": '#a90e0e'
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "meet_day": {
                "value": meet_days,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": "#6c6c6c"
            },
            "note_ch": {
                "value": note_ch,
                "color": "#6c6c6c"
            },

            # "pipi": {
            #     "value": pipi,
            #     "color": get_color()
            # },
            #
            # "lizhi": {
            #     "value": lizhi,
            #     "color": get_color()
            # },

            "pop": {
                "value": pop,
                "color": get_color()
            },
            "real": {
                "value": real,
                "color": get_color()
            },
            "wind": {
                "value": wind,
                # "color": get_color()
            },
            "windsc": {
                "value": windsc,
                "color": get_color()
            },
            "humidity": {
                "value": humidity,
                "color": '#1f71b3'
            },
            "uvindex": {
                "value": uvindex,
                "color": "#482881"
            },
            "temptips": {
                "value": temperatureTips,
                "color": "#bf1965"
            },
            "raintips": {
                "value": rainTips,
                "color": "#202b6a"
            },
            "lovetips": {
                "value": loveTips,
                "color": "#f91864"
            },
            'weektips': {
                "value": weekTips,
                "color": "#af8405"
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    province, city = config["province"], config["city"]
    # weather, max_temperature, min_temperature = get_weather(province, city)
    # 获取彩虹屁API
    caihongpi_API = config["caihongpi_API"]
    # 获取励志古言API
    # lizhi_API = config["lizhi_API"]
    # 获取天气预报API
    tianqi_API = config["tianqi_API"]
    # 是否启用词霸每日金句
    Whether_Eng = config["Whether_Eng"]
    # 获取词霸每日金句
    note_ch, note_en = get_ciba()
    # 彩虹屁
    # pipi = caihongpi()
    # 下雨概率和建议
    weather, real, max_temperature, min_temperature, pop, wind, windsc, humidity, uvindex = tip()
    # 励志名言
    # lizhi = lizhi()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, city, weather, real, max_temperature, min_temperature, pop, wind,
                     windsc, humidity, uvindex, note_en, note_ch)
    import time

    time_duration = 3.5
    time.sleep(time_duration)
