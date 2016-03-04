import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://www.qiushibaike.com/hot/'
contents = []
votes = []
n = 0

def download_pags(url):
    resp = requests.get(url).content
    return resp


def parse_html(html):
    global n
    soup = BeautifulSoup(html, 'lxml')
    joke_list = soup.find_all('div', 'article block untagged mb15')
    for joke in joke_list:
        vote = joke.find('i', 'number').getText()
        content = joke.find('div', 'content').getText().strip()
        votes.append(int(vote))
        contents.append(content)
        n += 1
    next_page = soup.find('span', 'next')
    next_page_final = next_page.find_parent('a')['href']
    if next_page_final == '/week':
        return None
    else:
        return DOWNLOAD_URL[:-5] + next_page_final


def final():
    p = 1
    with open('E:/糗百24hTop10.doc', 'w') as f:
        while p <= 10:
            vote = max(votes)
            s = votes.index(vote)
            content = contents[s]
            f.write(str(p) + content + '\n\n')
            print(vote, content)
            votes.remove(vote)
            p += 1


def main():
    url = DOWNLOAD_URL
    while url:
        html = download_pags(url)
        url = parse_html(html)
    final()


if __name__ == '__main__':
    main()