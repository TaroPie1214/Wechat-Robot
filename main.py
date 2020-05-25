from PyWeChatSpy import WeChatSpy
import requests
from weather import *
import re
from searchPics import *

#wxrobot框架

def get_reply(data):
    # key获取地址http://xiao.douqq.com/
    url = f"http://api.douqq.com/?key=dUk1cEtUdmZxc2RCPW5XaFdBdT1lWUJiSnhzQUFBPT0&msg={data}"
    resp = requests.get(url)
    return resp.text

#临时接口（待修改）
##需要与Anthony的代码接洽

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
            #如果收到图片搜索指令
            elif re.match('图片：(\w){1,20}', content):
                reply = '图片搜索结果：'
                downloadPic(content, 3)  #下载 
                for i in range(1, 4): #回传给客户端
                    spy.send_file("指定的wxid", 'download/images/%0.3d.jpg' % i)
            else:
                reply = get_reply(content)
                print(reply)
            spy.send_text("指定的wxid", reply)
    elif data["type"] == 2:
        print(data)

if __name__ == '__main__':
    spy = WeChatSpy(parser=parser)
    spy.run()
