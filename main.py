import requests  # 发送请求
import pandas as pd  # 保存csv文件
import os  # 判断文件是否存在
import time
from time import sleep  # 设置等待，防止反爬
import random  # 生成随机数
import hashlib
import string
import csv
from urllib.parse import quote
import re

# 请求头
headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 需定期更换cookie，否则location爬不到
    'cookie': "buvid3=7CB371E6-523F-7B91-E026-7AE3027AC9E096513infoc; b_nut=1682168696; CURRENT_FNVAL=4048; "
              "_uuid=D510B972B-D651-9E3F-D12A-77D7E6BED106795996infoc; "
              "CURRENT_PID=4782f570-e10e-11ed-bd27-7bbe4ef76ee9; rpdid=|(k))k)YYR|)0J'uY)kuY)Ym~; "
              "DedeUserID=12465574; DedeUserID__ckMd5=2686341d0ec8a6f8; "
              "buvid4=9155B8BB-2511-ECF7-4C77-3F1C079503C897197-023042221-tfXBzY9mGsKo%2FxsaI314xQ%3D%3D; "
              "buvid_fp_plain=undefined; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO5016822501062701; "
              "nostalgia_conf=-1; hit-new-style-dyn=1; hit-dyn-v2=1; enable_web_push=DISABLE; "
              "header_theme_version=CLOSE; CURRENT_QUALITY=80; home_feed_column=4; PVID=1; "
              "FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; fingerprint=ce4151136f44524bfb47a4dd4fbb55cc; "
              "browser_resolution=1360-687; "
              "SESSDATA=e5f82408%2C1728045636%2C7e35b"
              "%2A42CjCVJHZ4C9itKa7_kogjma8gOZhuHMZOyS77Jqd6nGShJ4R6VIrbDYtJ9YAlobQ94D4SVnlCQUZaOTBIWFlxdWFFYkMxQTBXam1vSmU2cmhOOXRuQ3N0THRKTEZDMFFBbWYwR3dlUkdJUlZlc3VVaXdETnpHLWtGakhYcnMtRVBock5lTlBHYmlRIIEC; bili_jct=ffada9921ffac5e6da95d4c28ac5cf15; sid=6bgcf3ir; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTI3NzUzNjgsImlhdCI6MTcxMjUxNjEwOCwicGx0IjotMX0.lH7U1hTS3QrYqlhz33_iBgJnYJbHRi6SpM9YguvVts0; bili_ticket_expires=1712775308; b_lsid=56510109F5_18EBF4F58D2; buvid_fp=ce4151136f44524bfb47a4dd4fbb55cc; bp_video_offset_12465574=918102061880442903",
    'origin': 'https://www.bilibili.com',
    'referer': 'https://t.bilibili.com/915271360576487425?spm_id_from=333.999.0.0',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
}


def new_url(offset):
    pagination_str = ("pagination_str=%7B%22offset%22%3A%22%7B%5C%22type%5C%22%3A3%2C%5C%"
                      "22direction%5C%22%3A1%2C%5C%22Data%5C%22%3A%7B%5C%22cursor%5C%22%3A") + offset + "%7D%7D%22%7D"
    Time = time.time()
    wts = "wts=" + str(round(Time))
    Wt = "ea1db124af3c7062474693fa704f4ff8"
    Zt = [
    "mode=2",
    "oid=915271360576487425",
    pagination_str,
    "plat=1",
    "type=17",
    "web_location=1315875",
    wts
]
    Jt = '&'.join(Zt)
    String = Jt + Wt
    MD5 = hashlib.md5()
    MD5.update(String.encode('utf-8'))
    w_rid = MD5.hexdigest()
    #print(w_rid)
    url = ("https://api.bilibili.com/x/v2/reply/wbi/main?oid=915271360576487425&type=17&mode=2&" + pagination_str + "&plat=1&web_location=1315875&w_rid=" + w_rid + "&" + wts)
    return url


# 创建 CSV 文件并写入表头
with open('comments.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['comment', 'member']  # 列名
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# 循环爬取评论数据并写入 CSV 文件
i = 0
cursor = "267930"

while True:
    i = i + 1
    print(i)
    url = new_url(cursor)
    print(url)
    response = requests.get(url, headers=headers)  # 发送请求
    data_list = response.json()['data']['replies']  # 解析评论数据
    offset = response.json()['data']['cursor']['pagination_reply']['next_offset']
    cursor = re.findall('cursor\":(\d+)', offset)[0]
    print(cursor)
    comment_list = []  # 评论内容空列表

    # 打开 CSV 文件并追加写入数据，使用 'a' 模式进行续写
    with open('comments.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, escapechar='\\')

        # 循环爬取每一条评论数据
        for a in data_list:
            # 评论内容
            comment = a['content']['message']
            member = a['member']['uname']
            comment_list.append(comment)
            # 实时将评论写入 CSV 文件
            writer.writerow({'comment': comment, 'member': member})

    print(comment_list[0])
    sleep(0.5)
