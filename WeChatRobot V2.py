from PyWeChatSpy import WeChatSpy
import json
import requests

try_times = 0
ar_times = 0
temp_times = 0

def parser(data):
    def tryTuLin(current_content, number_wxid):
        urls = 'http://openapi.tuling123.com/openapi/api/v2'  #请求地址
        data_dic = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": current_content
                },
                "inputImage": {
                    "url": "imageUrl"
                },
            },
            "userInfo": {
                "apiKey": "复制你的api到这里",
                "userId": number_wxid
            }
        }
        data_json = json.dumps(data_dic).encode('utf8')
        a = requests.post(urls, data_json)  # 使用post请求
        content = (a._content).decode('utf-8')  # 获取返回结果_content属性，解码
        res = json.loads(content)['results'] # 反序列化
        for i in res:
            back_content = i['values']['text']
        print(back_content)
        spy.send_text(current_wxid, back_content)
        return back_content

    #由于userid要求必须是是int类型，而wxid本身是一个字符串类型，这里通过将字符串中的每个字符
    # 转换成asc码再累加，实现了在满足int类型的同时，转化后的id也可以一一对应
    def wxidtonumber(current_wxid):
        number_wxid = 0
        for i in current_wxid:
            number_wxid += ord(i) #返回字符对应的ASCII
        return number_wxid

    print(data)

    if 'data' in data:  # 因为如果没收到内容则不会传回data，所以当收到内容时再执行下列语句
        for item in data['data']:
            current_self = item['self']  # self为0则为收到内容，为1则为发出内容
            current_wxid = item['wxid1']  # 对方的wxid
            current_content = item['content']  # 收到的内容

        global temp_content, temp_times, ar_times
        if temp_times == 0:  # temp_times默认值为0
            temp_content = current_content  # 赋值
            temp_times += 1  # 防止再次执行
        if temp_content != current_content:  # data中的content刷新，意味着收到了新的内容
            ar_times = 0  # 赋值为0
            temp_content = current_content  # 赋值
        if current_self == 0:
            if ar_times == 0:  # 值为0时才继续执行
                content1 = '已收到!'
                number_wxid = wxidtonumber(current_wxid)  # wxid从字符串通过编码转换为纯数字
                tryTuLin(current_content, number_wxid)  # 调用图灵机器人api自动回复
                print('auto send success')  # 控制台打印自动回复成功
                ar_times += 1  # 防止再次执行
        # 变量temp_times以及ar_times都是为了防止再次执行
        # temp_times存在的意义是实现程序开始后第一次执行
        # ar_times存在的意义是当data中的content发生改变时，再调用api
    else:
        raise Exception

if __name__ == '__main__':
    try:
        spy = WeChatSpy(parser=parser)
        spy.run()
    except Exception as e:
        print(e)