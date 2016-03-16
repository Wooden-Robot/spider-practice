import requests
from bs4 import BeautifulSoup


download_url = 'https://book.douban.com/top250'


# html下载器
def html_downloder(url):
    res = requests.get(url).text
    return res

# html解析器
def html_parser(html):
    books = []
    soup = BeautifulSoup(html, 'lxml')
    book_content = soup.find('div', 'indent')
    book_list = book_content.find_all('table', width='100%')
    for book in book_list:
        book_name = book.find('div', 'pl2').find('a')['title']
        book_star = book.find('span', 'rating_nums').getText()
        if float(book_star) > 8.0:
            books.append(book_name)
    next_page = soup.find('link', rel='next')
    if next_page:
        return books, next_page['href']
    else:
        return books, None

# 调度中心
def spider_main():
    url = download_url
    with open('豆瓣top250中评分8.0以上的书.txt', 'w') as f:
        while url:
            html = html_downloder(url)
            books, url = html_parser(html)
            for book in books:
                f.write(book+'\n')


if __name__ == '__main__':
    spider_main()