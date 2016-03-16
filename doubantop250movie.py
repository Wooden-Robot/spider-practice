#!/usr/bin/env python
#encoding=utf-8

from urllib import request
from bs4 import BeautifulSoup


DOWNLOAD_URL = 'http://movie.douban.com/top250'


# html下载器
def download_page(url):
    data = request.urlopen(url).read()
    return data.decode('utf-8')

# html解析器
def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):

        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()

        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None


def main():
    url = DOWNLOAD_URL
    n = 0

    with open('movies.txt', 'w') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            for m in movies:
                n += 1
                fp.write(str(n)+' '+m+'\n')
            print(movies, url)


if __name__ == '__main__':
    main()