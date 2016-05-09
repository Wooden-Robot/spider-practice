#!usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'woodenrobot'


import time
import re
import requests
from bs4 import BeautifulSoup

download_url = 'http://www.zhihu.com/collection/38624707'
p = 1
j = 0

# html下载器
def html_downloader(url):
    res = requests.get(url)
    return res.content


# html解析器
def html_parser(html):
    global j
    soup = BeautifulSoup(html, 'lxml')
    content_list = soup.find_all('div', class_='zm-item')
    print(len(content_list))
    for content in content_list:
        title = content.find('h2', class_='zm-item-title')
        if not title:
            pass
        else:
            filename = title.getText()
            print('--------正在爬取第{1}页问题{0}--------'.format(title.getText(), p))
        author = content.find('a', class_='author-link')
        if author:
            author = author.getText()
        else:
            author = '知乎用户'
        print('正在爬取第{1}页{0}的答案'.format(author, p))
        hide_content = content.find('textarea')
        imgs = re.findall(r'src="(.*?)"', str(hide_content))
        for img in imgs:
            print('-------------------------第{0}张-------------------------'.format(j))
            j += 1
            pic = requests.get(img).content
            with open('/home/woodenrobot/Downloads/pictures/'+str(j)+author+'.jpg', 'wb') as f:
                f.write(pic)
                # time.sleep(3)
                f.close()
    next_url = soup.find('a', text='下一页')
    if next_url:
        return download_url+next_url['href']
    else:
        return None


def main():
    global p
    url = download_url
    while url:
        html = html_downloader(url)
        url = html_parser(html)
        p += 1


if __name__  == '__main__':
    main()