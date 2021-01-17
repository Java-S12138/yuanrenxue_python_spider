# @BY     :Java_S
# @Time   :2021/1/15 18:00
# @Slogan :够坚定够努力大门自然会有人敲,别怕没人赏识就像三十岁的梵高

import re
import cv2
import requests
import base64
import numpy as np

def erode_image(img):
    # cv2.imread读取图像
    im = cv2.imread(img)
    # img.shape可以获得图像的形状，返回值是一个包含行数，列数，通道数的元组 (100, 100, 3)
    h, w = im.shape[0:2]
    # 去掉黑椒点的图像
    # np.all()函数用于判断整个数组中的元素的值是否全部满足条件，如果满足条件返回True，否则返回False
    im[np.all(im == [0, 0, 0], axis=-1)] = (255, 255, 255)
    # reshape：展平成n行3列的二维数组
    # np.unique()该函数是去除数组中的重复数字，并进行排序之后输出
    colors, counts = np.unique(np.array(im).reshape(-1, 3), axis=0, return_counts=True)
    # 筛选出现次数在500~2200次的像素点
    # 通过后面的操作就可以移除背景中的噪点
    info_dict = {counts[i]: colors[i].tolist() for i, v in enumerate(counts) if 500 < int(v) < 2200}

    # 移除了背景的图片
    remove_background_rgbs = info_dict.values()
    mask = np.zeros((h, w, 3), np.uint8) + 255# 生成一个全是白色的图片
    # 通过循环将不是噪点的像素,赋值给一个白色的图片,最后到达移除背景图片的效果
    for rgb in remove_background_rgbs:
        mask[np.all(im == rgb, axis=-1)] = im[np.all(im == rgb, axis=-1)]
    # cv2.imshow("Image with background removed", mask)  # 移除了背景的图片

    # 去掉线条,全部像素黑白化
    line_list = []# 首先创建一个空列表,用来存放出现在间隔当中的像素点
    # 两个for循环,遍历9000次
    for y in range(h):
        for x in range(w):
            tmp = mask[x, y].tolist()
            if tmp != [0, 0, 0]:
                if 110 < y < 120 or 210 < y < 220:
                    line_list.append(tmp)
                if 100 < x < 110 or 200 < x < 210:
                    line_list.append(tmp)
    remove_line_rgbs = np.unique(np.array(line_list).reshape(-1, 3), axis=0)
    for rgb in remove_line_rgbs:
        mask[np.all(mask == rgb, axis=-1)] = [255, 255, 255]
    # np.any()函数用于判断整个数组中的元素至少有一个满足条件就返回True，否则返回False。
    mask[np.any(mask != [255, 255, 255], axis=-1)] = [0, 0, 0]
    # cv2.imshow("Image with lines removed", mask)  # 移除了线条的图片

    # 腐蚀
    # 卷积核涉及到python形态学处理的知识,感兴趣的可以自行百度
    # 生成一个2行三列数值全为1的二维数字,作为腐蚀操作中的卷积核
    kernel = np.ones((2, 3), 'uint8')
    erode_img = cv2.erode(mask, kernel, cv2.BORDER_REFLECT, iterations=2)
    cv2.imshow('Eroded Image', erode_img)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()可以轻易删除任何我们建立的窗口，括号内输入想删除的窗口名
    cv2.destroyAllWindows()
    cv2.imwrite('image/deal.png', erode_img)
    return 'image/deal.png'

def get_verify(session):
    url = 'http://match.yuanrenxue.com/api/match/8_verify'
    response = session.get(url)

    html_str = response.json()['html']

    words_data = re.compile(r'<p>(.*?)</p>')
    words = words_data.findall(html_str)
    image_data = re.compile(r'src="(.*?)"')
    image_base64 = image_data.findall(html_str)[0].replace('data:image/jpeg;base64,','')
    with open('image/web_img.png', 'wb') as f:
        f.write(base64.b64decode(image_base64.encode()))
    print(words)
    return words

def get_page(page_num,index_list,session):
    url = 'http://match.yuanrenxue.com/api/match/8'
    click_dict = {
        '1':126,'2':136,'3':146,
        '4':426,'5':466,'6':477,
        '7':726,'8':737,'9':776
    }
    answer = '|'.join([str(click_dict[i]) for i in index_list])+'|'
    params = {
        'page':page_num,
        'answer':answer
    }
    response = session.get(url=url,params=params)
    try:
        value_list = [i['value'] for i in response.json()['data']]
        print(f'第{page_num}页的值为:{value_list}')
        return value_list
    except:
        print(f'第{page_num}页验证失败')
        return []



if __name__ == '__main__':
    session = requests.session()
    session.headers = {'User-Agent': 'yuanrenxue.project'}
    answer_list=[]

    for i in range(1,6):
        words = get_verify(session)
        erode_image(r'image/web_img.png')
        word_dict = input('请输入对应的坐标:')
        answer_list.extend(get_page(i, list(word_dict), session))

    print(f'出现次数最多的数字是:{max(set(answer_list), key=answer_list.count)}')