# @BY     :Java_S
# @Time   :2020/12/26 12:14
# @Slogan :够坚定够努力大门自然会有人敲,别怕没人赏识就像三十岁的梵高

import requests
import execjs
import time

def get_cipher_value():
    # 导入JS,读取需要的js文件
    with open(r'JS/jsCookie.js',encoding='utf-8',mode='r') as f:
        JsData = f.read()
    # 加载js文件,使用call()函数执行,传入需要执行函数即可获取返回值
    psd = execjs.compile(JsData).call('get_cipher')
    return psd

def get_data(page_num,cipher):
    url = f'http://match.yuanrenxue.com/api/match/2?page={page_num}'
    headers = {
        'Host': 'match.yuanrenxue.com',
        'User-Agent':'yuanrenxue.project',
        'Cookie':cipher
    }
    print(f'加密密文--->{cipher}')
    response = requests.get(url,headers = headers)
    return response.json()


if __name__ == '__main__':

    sum_num = 0

    for page_num in range(1, 6):
        info = get_data(page_num, get_cipher_value())
        price_list = [i['value'] for i in info['data']]
        print(f'第{page_num}页发布日热度的值:{price_list}')
        sum_num += sum(price_list)
        time.sleep(1)

    print(f'发布日热度值总和:{sum_num}')
