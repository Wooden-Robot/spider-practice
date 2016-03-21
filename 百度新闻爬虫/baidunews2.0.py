import json
import requests
from bs4 import BeautifulSoup


download_url = 'http://news.baidu.com/ns'
final_contents = {}
n = 1


def word():
    global x
    x = input('请输入搜索关键词：')
    payload = {'word': x}
    return payload


# html下载器
def html_downloader(url, payload):
    res = requests.get(url, params=payload)
    print('Downloading', res.url)
    return res.content


# html解析器
def html_parser(html):
    global n
    contents = {}
    soup = BeautifulSoup(html, 'lxml')
    content_list = soup.find_all('div', class_='result')
    for content in content_list:
        # 获取标题
        title = content.find('a', target='_blank').stripped_strings
        title = ''.join(title)
        # 获取来源和时间：
        time_from = content.find('p', class_="c-author").string
        type(time_from)
        time_from = time_from.replace('\xa0\xa0', ', ')
        # 获取摘要：
        content.find('p', 'c-author').extract()
        content.find('span', 'c-info').extract()
        content.find('h3', 'c-title').extract()
        summary = ''.join(content.stripped_strings)
        # 储存数据：
        contents[n] = {}
        contents[n]['title'] = title
        contents[n]['time_from'] = time_from
        contents[n]['sumary'] = summary
        n += 1
    next_page = soup.find('strong').next_sibling
    if next_page:
        return contents, download_url[0:-3] + next_page['href']
    else:
        return contents, None


# 调度中心
def spider_main():
    global final_contents
    url = download_url
    payload = word()
    while url:
        html = html_downloader(url, payload)
        contents, url = html_parser(html)
        # 获取的url已包含word参数，无需继续添加。
        payload = {}
        final_contents.update(contents)
    final_contents = json.dumps(final_contents, ensure_ascii=False)
    print(final_contents)


if __name__ == '__main__':
    spider_main()