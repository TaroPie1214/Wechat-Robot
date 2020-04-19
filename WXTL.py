from PyWeChatSpy import WeChatSpy
import time
import json
import requests

try_times = 0
artimes = 0
temp_times = 0

def parser(data):
    def tryTuLin(current_content,number_wxid):
        urls = 'http://openapi.tuling123.com/openapi/api/v2'  # 请求地址
        data_input = current_content
        data_dic = {
	        "reqType":0,
            "perception": {
                "inputText": {
                    "text": data_input
                },
                "inputImage": {
                    "url": "imageUrl"
                },
            },
            "userInfo": {
                "apiKey": "0bc0e8729d68490883deb2734b69c23f",
                "userId": number_wxid
            }
        }
        data_json = json.dumps(data_dic).encode('utf8')
        a = requests.post(urls,data_json)  # 使用post请求
        content = (a._content).decode('utf-8')  # 获取返回结果_content属性，解码
        res = json.loads(content)  # 反序列化
        mb = res['results']
        for item in mb:
            mb2 = item
        mb3 = mb2['values']
        print(mb3['text'])
        back_content = mb3['text']
        spy.send_text(current_wxid, back_content)
        return back_content

    def wxidtonumber(current_wxid):
        b = 0
        for i in current_wxid:
            c = ord(i)
            b += c
        number_wxid = b
        return number_wxid

    print(data)

    #wxid = 'filehelper'
    #content = 'test'

    #global try_times
    #if try_times <= 1:
    #    spy.send_text(wxid, content)
    #    print('send success')
    #    try_times += 1



    if 'data' in data:  #因为如果没收到内容则不会传回data，所以当收到内容时再执行下列语句
        nb = data['data']
        #print (nb)
        for item in nb:
            nb2 = item
        print (nb2)  #这个传回来的data很复杂，上面的步骤就是从中提取出nb2这个字典
        #print (nb2['self'])
        current_self = nb2['self']  #self为0则为收到内容，为1则为发出内容
        current_wxid = nb2['wxid1']  #对方的wxid
        current_content = nb2['content']  #收到的内容
        global temp_content
        global temp_times
        if temp_times == 0:  #temp_times默认值为0
            temp_content = current_content  #赋值
            temp_times += 1  #防止再次执行
        if temp_content != current_content:  #data中的content刷新，意味着收到了新的内容
            global artimes
            artimes = 0  #赋值为0
            temp_content = current_content  #赋值
        if current_self == 0:
            if artimes == 0:  #值为0时才继续执行
                content1 = '已收到!'
                #back_content = ""      
                number_wxid = wxidtonumber(current_wxid)  #wxid从字符串通过编码转换为纯数字
                tryTuLin(current_content,number_wxid)  #调用图灵机器人api自动回复               
                #spy.send_text(current_wxid, content1)
                print('auto send success')  #控制台打印自动回复成功
                artimes += 1  #防止再次执行
        #变量temp_times以及artimes都是为了防止再次执行
        #temp_times存在的意义是实现程序开始后第一次执行
        #artimes存在的意义是当data中的content发生改变时，再调用api
                
if __name__ == '__main__':
    spy = WeChatSpy(parser=parser)
    spy.run()

#wxid_1157791577711
#wxid_1fbf89webaor12