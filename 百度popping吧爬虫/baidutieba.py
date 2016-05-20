#!usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'woodenrobot'

import requests
import json
import threading, multiprocessing
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime


# 生成爬取网页url列表
url_list = list(('http://tieba.baidu.com/f?kw=poppin&ie=utf-8&pn=%d'
                %num for num in range(0, 79950, 50)))
j = 0


# html下载器
def html_downloader(url):
    res = requests.get(url)
    return res.content


# html 解析器
def html_parser(url, html):
    soup = BeautifulSoup(html, 'lxml')
    content_list = soup.find_all('li', class_=' j_thread_list clearfix')
    for content in content_list:
        data = {}
        data_field = content['data-field']
        data_field = json.loads(data_field)
        data['_id'] = data_field['id']
        data['author_name'] = data_field['author_name']
        data['reply_num'] = data_field['reply_num']
        title = content.find('a', class_='j_th_tit ')
        data['title'] = title['title']
        data['url'] = 'http://tieba.baidu.com/' + title['href']
        sumary = content.find('div', class_='threadlist_abs threadlist_abs_onlyline ')
        if sumary:
            data['sumary'] = sumary.string.replace('\n', '').strip(' ')
        imgs = content.find_all('img')
        # 图片可能有有三个地址，也可能有一个或者没有
        if imgs:
            img_list = []
            for img in imgs:
                try:
                    img_list.append(img['bpic'])        #高清大图地址
                except:
                    try:
                        img_list.append(img['data-original'])   #缩略图地址
                    except:
                        if img['src'] != '':        #src存在空值现象，将空值剔除
                            img_list.append(img['src'])
            data['imgs'] = img_list
        video = content.find('a', class_='threadlist_btn_play j_m_flash')
        if video:
            data['video'] = video['data-video']
        data['updateTime'] = datetime.datetime.now()
        # 将获取的数据存入Mongodb数据库
        MONGO_CONN = MongoClient('localhost', 27017)
        MONGO_CONN['database']['popping'].update_one(
        filter={'_id': data['_id']},
        update={'$set': data},
        upsert=True
        )


def main():
    global j
    while True:
        html = html_downloader(url_list[j])
        html_parser(url_list[j], html)
        print('------------------正在获取第{0}页内容------------------'.format(j+1))
        if url_list[j] == 'http://tieba.baidu.com/f?kw=poppin&ie=utf-8&pn=79850':
            print('*********************所有页面爬取完毕********************')
            break
        j += 1


if __name__ == '__main__':
   main()