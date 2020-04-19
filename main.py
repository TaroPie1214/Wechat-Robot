from PyWeChatSpy import WeChatSpy
import requests
from weather import *
import re

#wxrobot框架

def get_reply(data):
    # key获取地址http://xiao.douqq.com/
    url = f"http://api.douqq.com/?key=dUk1cEtUdmZxc2RCPW5XaFdBdT1lWUJiSnhzQUFBPT0&msg={data}"
    resp = requests.get(url)
    return resp.text

#临时接口（待修改）

def parser(data):
    if data["type"] == 1:
        print(data)
    elif data["type"] == 200:
        # 心跳
        pass
    elif data["type"] == 203:
        print("微信退出登录")
    elif data["type"] == 5:
        # 消息
        for item in data["data"]:
            content = item["content"]
            print(content)
            #如果收到内容格式为xx天气，正则匹配
            if re.match('(\w){1,10}天气', content):
                #调用weather函数
                reply = reply_weather(content)
                print(reply)
            else:
                reply = get_reply(content)
                print(reply)
            spy.send_text("wxid_3xollkhxgq5t22", reply)
    elif data["type"] == 2:
        print(data)

if __name__ == '__main__':
    spy = WeChatSpy(parser=parser)
    spy.run()



