# @BY     :Java_S
# @Time   :2021/1/3 18:30
# @Slogan :够坚定够努力大门自然会有人敲,别怕没人赏识就像三十岁的梵高

import re
import requests

def get_data(page):
    url = 'http://match.yuanrenxue.com/match/13'
    response = requests.get(url)
    cookie = ''.join(re.findall(r"'(.*?)'", response.text))[:-7]
    sessionid = response.headers['Set-Cookie'].split(';')[0]

    url_api = f'http://match.yuanrenxue.com/api/match/13?page={page}'
    headers = {
        'User-Agent': 'yuanrenxue.project',
        'Cookie': sessionid+';'+cookie
    }
    res = requests.get(url=url_api,headers=headers)
    return res.json()['data']

if __name__ == '__main__':
    nums_sum = []
    for i in range(1, 6):
        data = [i['value'] for i in get_data(i)]
        nums_sum.extend(data)
    print(f'五页数字总和:{sum(nums_sum)}')
