import re
import requests
import os
import random

def downloadPic(keyword, number):
    keyword = keyword[3:]  #取出关键字
    os.makedirs('download/images', exist_ok=True) #服务端下载到文件夹 
    ##可以考虑以后加入mysql进行数据库整理
    
    rand = random.randint(1, 100) 
    ##先设置一个随机数，下面这个url里面 把keyword关键字搞进去 再之后通过变量绑定把pn的值设置为那个随机数
    ##pn意义相当于图片位置，目的在于从网页爬图片的时候不重复 在前一百张以内
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + f'&ct=201326592&v=flip&pn={rand}'
    result = requests.get(url)
    print(result)
    html = result.text #拿到返回数据

    pic_url = re.findall('"objURL":"(.*?)",', html, re.S) #正则 找到所有objURL 即图片数据
    i = 1
    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for each in pic_url:
        if i > number:
            return #迭代出域 返回空退出

        print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10) #get方法拿到pic数据 设置timeout为10s
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')   
            continue   #遇到下载不行的直接跳过继续

        fp = open('download/images/%0.3d.jpg' % i, 'wb')
        fp.write(pic.content) #文件流写入图片
        fp.close()
        i += 1 #迭代i
