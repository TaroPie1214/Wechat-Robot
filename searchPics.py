import re
import requests
import os
import random

def downloadPic(keyword, number):
    keyword = keyword[3:]
    os.makedirs('download/images', exist_ok=True)
    rand = random.randint(1, 100)
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + f'&ct=201326592&v=flip&pn={rand}'
    result = requests.get(url)
    print(result)
    html = result.text

    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    i = 1
    x = number
    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for each in pic_url:
        if i > x:
            return

        print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')
            continue

        fp = open('download/images/%0.3d.jpg' % i, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1
