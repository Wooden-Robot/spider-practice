import requests
from bs4 import BeautifulSoup

# 构造Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, ' \
        'like Gecko) Chrome/48.0.2564.116 Safari/537.36'
headers = {
    'User-Agent': agent
}

s = requests.session()
def get_xsrf():
    '''xsrf是一个动态的值，每次登陆前都要重新获取'''
    r = s.get('https://www.zhihu.com/', headers=headers).content
    soup = BeautifulSoup(r)
    _xsrf = soup.find('input', attrs={'type': 'hidden'})['value']
    return _xsrf

def login():
    '''判断账号为手机号或者邮箱模拟登陆知乎'''
    username = input('请输入邮箱或手机：')
    password = input('请输入密码：')
    if '@' in username:
        post_url = 'http://www.zhihu.com/login/email'
        payload = {
            '_xsrf': get_xsrf(),
            'password': password,
            'remember_me': 'true',
            'email': username
        }
    else:
        post_url = 'http://www.zhihu.com/login/phone_num'
        payload = {
            '_xsrf': get_xsrf(),
            'password': password,
            'remember_me': 'true',
            'phone_num': username
        }
    r = s.post(post_url, data=payload)
    return s


if __name__ == '__main__':
    s = login()
    # 判断是否登陆成功
    question = BeautifulSoup(s.get('https://www.zhihu.com/')
                             .content).find('a', 'question_link').getText()
    print(question)
