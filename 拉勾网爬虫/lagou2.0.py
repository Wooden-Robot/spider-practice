#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'woodenrobot'

import requests
import json
import datetime
import time
import random
from pymongo import MongoClient
from lagou_job_list import spider_manager


n = 1
job = ''
s = ["http://111.206.190.155:80",
     "http://58.252.2.5:8003"]
ip = random.choice(s)
proxies = {"http": ip}
MONGO_CONN = MongoClient('localhost', 27017)


def download_page():
    global n, job
    print('*******************正在爬取'+job+'第{0}页******************'.format(n))
    if n == 1:
        sth = 'true'
    else:
        sth = 'false'
    login_data = {'first': sth, 'pn': str(n), 'kd': job}
    try:
        print('代理ip为：', proxies)
        res = requests.post('http://www.lagou.com/jobs/positionAjax.json?px='
                            'new&needAddtionalResult=false',
                             data=login_data, proxies=proxies).text
        time.sleep(0.3)
    except:
        print('*******************第{0}页失败,重新爬取*******************'.format(n))
        res = requests.post('http://www.lagou.com/jobs/positionAjax.json?px='
                            'new&needAddtionalResult=false',
                             data=login_data, proxies=proxies).text
    # print(res)
    n += 1
    json_obj = json.loads(res)
    s = json_obj['content']['positionResult']['result']
    return s


def save(datas):
    for data in datas:
        # print(data['positionId'])
        data['updataTime'] = datetime.datetime.now()
        MONGO_CONN['database']['lagou2'].update_one(
        filter={'_id': data["positionId"]},
        update={'$set': data},
        upsert=True
        )


def main():
    global job, n
    job_list = spider_manager()
    print(job_list)
    for job in job_list:
        job = job
        n = 1
        while n:
            s = download_page()
            if s == []:
                print('*******************'+job+'爬取完毕*******************')
                break
            print(s)
            save(s)

if __name__ == '__main__':
    main()