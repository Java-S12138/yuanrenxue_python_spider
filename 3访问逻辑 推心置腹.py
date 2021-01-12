# @BY     :Java_S
# @Time   :2020/12/31 15:45
# @Slogan :够坚定够努力大门自然会有人敲,别怕没人赏识就像三十岁的梵高

import requests
import pandas as pd


def get_data(page_num):
    session = requests.session()

    headers = {'Connection': 'keep-alive',
               'User-Agent': 'yuanrenxue.project',
               'Accept': '*/*',
               'Origin': 'http://match.yuanrenxue.com',
               'Referer': 'http://match.yuanrenxue.com/match/3',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
               }
    
    url = 'http://match.yuanrenxue.com/logo'
    session.headers = headers
    response = session.post(url=url)

    url_api = f'http://match.yuanrenxue.com/api/match/3?page={page_num}'
    res = session.get(url=url_api).json()
    data = [i['value'] for i in res['data']]
    return data


if __name__ == '__main__':
    data = []
    for i in range(1, 6):
        data_list = get_data(i)
        data.extend(data_list)
    count = pd.value_counts(data)
    print(count)
