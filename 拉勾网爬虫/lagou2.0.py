#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'woodenrobot'

import requests
import json
import datetime
import time
from pymongo import MongoClient


n = 1
MONGO_CONN = MongoClient('localhost', 27017)
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
#                          '(KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}


def download_page():
    global n
    print('*******************正在爬取第{0}页******************'.format(n))
    if n == 1:
        sth = 'true'
    else:
        sth = 'false'
    login_data = {'first': sth, 'pn': str(n), 'kd': 'Python'}
    try:
        res = requests.post('http://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false',
                             data=login_data, timeout=2).text
    except:
        print('*******************第{0}页失败,重新爬取*******************'.format(n))
        res = requests.post('http://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false',
                             data=login_data).text
    print(res)
    n += 1
    json_obj = json.loads(res)
    s = json_obj['content']['positionResult']['result']
    return s


def save(datas):
    for data in datas:
        print(data['positionId'])
        data['updataTime'] = datetime.datetime.now()
        MONGO_CONN['database']['lagou_Python'].update_one(
        filter={'_id': data["positionId"]},
        update={'$set': data},
        upsert=True
        )


def main():
    while n:
        s = download_page()
        if s == []:
            print('*******************爬取完毕*******************')
            break
        print(s)
        save(s)

if __name__ == '__main__':
    main()