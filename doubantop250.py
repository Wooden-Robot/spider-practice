#!/usr/bin/env python
#encoding=utf-8


import requests


DOWNLOAD_URL = 'http://movie.douban.com/top250'


def download_page(url):
    data = requests.get(url).text
    return data


def main():
    print(download_page(DOWNLOAD_URL))


if __name__ == '__main__':
    main()