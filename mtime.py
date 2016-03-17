import requests
import re
import json


url = 'http://service.library.mtime.com/Movie.api'
data = {'Ajax_CallBack': 'true',
        'Ajax_CallBackType': 'Mtime.Library.Services',
        'Ajax_CallBackMethod': 'GetMovieOverviewRating',
        'Ajax_CrossDomain': '1',
        'Ajax_CallBackArgument0':  '156682'}


# 网页下载器
def html_downloader(url):
    res = requests.get(url, data=data).text
    return res

# 解析器
def parser(contents):
    # 将所要的信息筛选出来
    content = ''.join(re.findall(r'{.*}', contents))
    # 将data从Json形式转换为字典
    datas = json.loads(content)
    star = datas['value']['movieRating']['RatingFinal']
    name = datas['value']['movieTitle']
    print(star, name)

def main():
    contents = html_downloader(url)
    print(contents)
    parser(contents)


if __name__ == '__main__':
    main()