#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'woodenrobot'

import requests
import json
import datetime
from pymongo import MongoClient


n = 1
login_data = {'first': 'true', 'pn': str(n), 'kd': 'python'}
MONGO_CONN = MongoClient('localhost', 27017)

def download_page(data):
    global n, login_data
    print('*******************正在爬取第{0}页******************'.format(n))
    if n == 1:
        sth = 'true'
    else:
        sth = 'false'
    login_data = {'first': sth, 'pn': str(n), 'kd': 'python'}
    data = requests.post('http://www.lagou.com/jobs/positionAjax.json?', data=data).text
    n += 1
    json_obj = json.loads(data)
    s = json_obj['content']['result'][1:17]
    return s


def save(datas):
    for data in datas:
        MONGO_CONN['database']['lagou'].update_one(
        filter={'_id': data["positionId"]},
        update={'$set': data},
        upsert=True
        )


def main():
    while n:
        s = download_page(login_data)
        if s == []:
            break
        save(s)

if __name__ == '__main__':
    main()