# @BY     :Java_S
# @Time   :2021/1/11 17:13
# @Slogan :够坚定够努力大门自然会有人敲,别怕没人赏识就像三十岁的梵高
import os
import re
import base64
import requests
from xml.dom.minidom import parse
from fontTools.ttLib import TTFont


def get_data(page):
    url = f'http://match.yuanrenxue.com/api/match/7?page={page}'
    headers = {'User-Agent': 'yuanrenxue.project'}

    response = requests.get(url=url, headers=headers)
    woff_data = response.json()['woff']
    value_data = response.json()['data']
    value_data = [re.findall(r"\d+\.?\d*", i['value'].replace('&#x', '').replace(' ', '')) for i in value_data]
    # 下载字体文件
    download_woff(woff_data)

    return value_data


def download_woff(woff_data, ):
    with open('cipher.woff', mode='wb') as file:
        file.write(base64.b64decode(woff_data.encode()))
    file.close()


def get_real_nums():
    cipher_nums = {'1010010010': 0, '1001101111': 1, '1001101010': 2,
                   '1010110010': 3, '1111111111': 4, '1110101001': 5,
                   '1010101010': 6, '1111111': 7, '1010101011': 8, '1001010100': 9}

    # 加载字体文件
    online_font = TTFont('cipher.woff')
    # 转为xml文件
    online_font.saveXML('cipher.xml')
    font = parse(r'cipher.xml')  # 读取xml文件
    xml_list = font.documentElement  # 获取xml文档对象，就是拿到DOM树的根
    # getElementsByTagName()
    # 获取xml文档中的某个父节点下具有相同节点名的节点对象的集合,返回的是list
    all_ttg = xml_list.getElementsByTagName('TTGlyph')[1:]
    cipher_dict = {}
    for TTGlyph in all_ttg:
        name = TTGlyph.getAttribute('name')[4:]  # 获取节点的属性值
        pt = TTGlyph.getElementsByTagName('pt')
        num = ''
        if (len(pt) < 10):
            for i in range(len(pt)):
                num += pt[i].getAttribute('on')
        else:
            for i in range(10):
                num += pt[i].getAttribute('on')
        num = cipher_nums[num]
        cipher_dict[name] = num

    return cipher_dict


def real_data(value_data, cipher_dict):
    num_list = []
    for data in value_data:
        num = ''
        for i in data:
            num += str(cipher_dict[i])
        num_list.append(int(num))
    return num_list


if __name__ == '__main__':
    rank_list = []

    for i in range(1, 6):
        real_num_list = real_data(get_data(i), get_real_nums())
        print(f'第{i}页胜点数据:{real_num_list}')
        rank_list.extend(real_num_list)
    print(f'最高的胜点数是:{max(rank_list)}')

    # 删除下载和转换的文件
    os.remove('cipher.xml')
    os.remove('cipher.woff')
