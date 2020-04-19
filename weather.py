import json
import requests
from urllib3 import *

disable_warnings()
http = PoolManager()

#回传天气数据函数
def reply_weather(content):
    #获取位置
    location = content[0:-2]
    #和风天气 api-key申请
    url = f'https://free-api.heweather.net/s6/weather/now?location={location}&key=8c321dd4895f4c32963c52e6aa3b0cfc'
    #request拿到所需json数据
    data = http.request('GET', url).data.decode('utf-8')
    data = json.loads(data)
    #状态码ok
    if data["HeWeather6"][0]['status'] == 'ok':
        data = data["HeWeather6"]
        res = '''
            查询位置：%s \n
            纬度：%s \n
            经度：%s \n
            温度：%s \n
            湿度：%s \n
            风向：%s \n
            天气情况：%s \n
            更新时间：%s \n
            ''' % (data[0]['basic']['location'], data[0]['basic']['lat'],
                   data[0]['basic']['lon'], data[0]['now']['tmp'], data[0]['now']['hum'],
                   data[0]['now']['wind_dir'], data[0]['now']['cond_txt'],
                   data[0]['update']['loc'])
    else:
        res = '获取天气失败，请按格式搜索“城市名+天气”'
    return res



