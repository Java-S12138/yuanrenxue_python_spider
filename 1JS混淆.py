# @BY     :Java_S
# @Time   :2020/12/25 9:10
# @Slogan :够坚定够努力大门自然会有人敲,别怕没人赏识就像三十岁的梵高

import requests
import execjs
import time

def get_md5_value():
    # 导入JS,读取需要的js文件
    with open(r'JS/jsConfuse.js',encoding='utf-8',mode='r') as f:
        JsData = f.read()
    # 加载js文件,使用call()函数执行,传入需要执行函数即可获取返回值
    psd = execjs.compile(JsData).call('get_cipher')
    psd = psd.replace('丨','%E4%B8%A8')
    return psd

def get_data(page_num,md5):
    url = f'http://match.yuanrenxue.com/api/match/1?page={page_num}&m={md5}'
    headers = {
        'Host':'match.yuanrenxue.com',
        'Referer':'http://match.yuanrenxue.com/match/1',
        'User-Agent':'yuanrenxue.project',
    }
    response = requests.get(url,headers=headers)
    return response.json()

if __name__ == '__main__':

    sum_num = 0
    index_num = 0

    for page_num in range(1,6):
        info = get_data(page_num,get_md5_value())
        price_list = [i['value'] for i in info['data']]
        print(f'第{page_num}页的价格列表{price_list}')
        sum_num += sum(price_list)
        index_num += len(price_list)
        time.sleep(1)

    average_price = sum_num / index_num
    print(f'机票价格的平均值:{average_price}')