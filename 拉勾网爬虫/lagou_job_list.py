#!usr/bin/env python
# coding: utf-8
__author__ = 'woodenrobot'


import requests
from bs4 import BeautifulSoup


DOWNLOAD_URL = 'http://www.lagou.com/'


def html_downloader(url):
    res = requests.get(url)
    return res.text


def html_parser(html):
    soup = BeautifulSoup(html, 'lxml')
    job_content = soup.find('div', class_='menu_sub dn')
    job_list = job_content.find_all('dt')
    for v in job_list:
        v.extract()
    return list(job_content.stripped_strings)


def spider_manager():
    url = DOWNLOAD_URL
    html = html_downloader(url)
    job_list = html_parser(html)
    return job_list


if __name__ == '__main__':
    spider_manager()