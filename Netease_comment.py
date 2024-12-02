# -*- coding: utf-8 -*-
import collections
import datetime
import requests, execjs, json
import time
import wordcloud
import jieba
import PIL.Image as image
import numpy as np
import matplotlib.pyplot as plt  # 图像展示库


import json
import time
import requests

headers = {
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def get_comments(page):
    """
        获取评论信息
    """
    url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_33937527?limit=20&offset=' + str(page)
    response = requests.get(url=url, headers=headers)
    # 将字符串转为json格式
    result = json.loads(response.text)
    items = result['comments']
    for item in items:

        # 用户名
        user_name = item['user']['nickname'].replace(',', '，')
        # 评论内容
        comment = item['content'].strip().replace('\n', '').replace(',', '，')
        date = time.localtime(int(str(item['time'])[:10]))
        date = time.strftime("%Y-%m-%d %H:%M:%S", date)
        #print(user_name, praise, date)

        with open('music_comments.csv', 'a', encoding='utf-8-sig') as f:
            f.write(user_name + ',' + comment + ',' + date + '\n')
        f.close()

def main():
    for i in range(0, 25000, 20):
        print('\n---------------第 ' + str(i // 20 + 1) + ' 页---------------')
        get_comments(i)


if __name__ == '__main__':
    main()