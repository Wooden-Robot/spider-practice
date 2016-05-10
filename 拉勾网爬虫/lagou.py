import requests
import json
import datetime


n = 1
login_data = {'first': 'true', 'pn': str(n), 'kd': 'python'}


def download_page(data):
    global n, login_data
    n += 1
    if n == 1:
        sth = 'true'
    else:
        sth = 'false'
    login_data = {'first': sth, 'pn': str(n), 'kd': 'python'}
    data = requests.post('http://www.lagou.com/jobs/positionAjax.json?', data=data).text
    json_obj = json.loads(data)
    s = json_obj['content']['result'][1:17]
    return s

def save(datas):
    for data in datas:
       print(n, data['companyShortName'], data)

def main():
    while n:
        s = download_page(login_data)
        if s == []:
            break
        save(s)



if __name__ == '__main__':
    main()
