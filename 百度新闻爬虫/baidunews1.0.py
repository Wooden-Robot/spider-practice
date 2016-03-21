import re
import json
import requests
from bs4 import BeautifulSoup



def word():
    x = input('请输入搜索关键词：')
    payload = {'word': x}
    return payload

# html下载器
def html_downloader(payload):
    res = requests.get('http://news.baidu.com/ns', params=payload).content
    return res

# html解析器
def html_parser(html):
    n = 1
    contents = {}
    soup = BeautifulSoup(html, 'lxml')
    content_list = soup.find_all('div', class_='result')
    for content in content_list:
        # 获取标题
        title = content.find('a', target='_blank').stripped_strings
        # 获取来源和时间：
        time_from = content.find('p', class_="c-author")
        from_ = re.search('^(.*?)\xa0\xa0(.*)$', time_from.string).group(1)
        time = re.search('^(.*?)\xa0\xa0(.*)$', time_from.string).group(2)
        # 获取摘要：
        summ = ''.join(content.strings)
        parten = time+'(.*?)\s'
        summary = re.search(parten, summ).group(1)
        # 储存数据：
        contents[n] = {}
        contents[n]['title'] = ''.join(title)
        contents[n]['from'] = from_
        contents[n]['time'] = time
        contents[n]['sumary'] = summary
        n += 1
    # 转换json格式
    contents = json.dumps(contents, ensure_ascii=False)
    print(contents)




# 调度中心
def spider_main():
    payload = word()
    html = html_downloader(payload)
    html_parser(html)


if __name__ == '__main__':
    spider_main()