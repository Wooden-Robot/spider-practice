#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'woodenrobot'

import requests
import json
import datetime
import time
from pymongo import MongoClient


n = 1
login_data = {'first': 'true', 'pn': str(n), 'kd': 'iOS'}
MONGO_CONN = MongoClient('localhost', 27017)
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
#                          '(KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}


def download_page(data):
    global n, login_data
    print('*******************正在爬取第{0}页******************'.format(n))
    if n == 1:
        sth = 'true'
    else:
        sth = 'false'
    login_data = {'first': sth, 'pn': str(n), 'kd': ''}
    try:
        data = requests.post('http://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false',
                             data=data, timeout=2).text
    except:
        print('*******************第{0}页失败,重新爬取*******************'.format(n))
        data = requests.post('http://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false',
                             data=data).text
    print(data)
    n += 1
    json_obj = json.loads(data)
    s = json_obj['content']['positionResult']['result']
    return s


def save(datas):
    for data in datas:
        data['updataTime'] = datetime.datetime.now()
        MONGO_CONN['database']['lagou'].update_one(
        filter={'_id': data["positionId"]},
        update={'$set': data},
        upsert=True
        )


def main():
    while n:
        s = download_page(login_data)
        if s == []:
            print('*******************爬取完毕*******************')
            break
        print(s)
        save(s)

if __name__ == '__main__':
    main()