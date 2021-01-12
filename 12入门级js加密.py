# @BY     :Java_S
# @Time   :2021/1/3 17:23
# @Slogan :够坚定够努力大门自然会有人敲,别怕没人赏识就像三十岁的梵高

import base64
import requests

def get_base64(page):
    base_str = 'yuanrenxue'+f'{page}'
    base_str = base_str.encode('ascii')
    base = base64.b64encode(base_str).decode('utf-8')
    return base

def get_data(page,m):
    url = f'http://match.yuanrenxue.com/api/match/12?page={page}&m={m}'
    headers = {'User-Agent': 'yuanrenxue.project'}
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    return data

if __name__ == '__main__':
    nums_sum = []
    for i in range(1,6):
        m = get_base64(i)
        data = [i['value'] for i in get_data(i,m)]
        nums_sum.extend(data)
    print(f'五页数字总和:{sum(nums_sum)}')