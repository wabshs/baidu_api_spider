import re

import requests
from bs4 import BeautifulSoup
import json


def get_html(url: str):
    # 转化为bs对象
    html_response = requests.get(url)
    html = html_response.text
    html_soup = BeautifulSoup(html, 'html.parser')

    # 然后可以开始爬元素了
    # 首先获取class为post__title的h1节点
    h1 = html_soup.find('h1', class_='post__title')
    api_name = h1.text
    print(api_name)

    # 再获取id为接口描述的<h2>节点
    h2 = html_soup.find('h2', {'id': '接口描述'})
    # 成功获取到api_description这个字段
    api_description = h2.find_next_sibling().text
    print(api_description)

    # 获取请求方式
    code = html_soup.find('code', class_='language-text')
    method = code.text
    print(method)

    base_url = code.find_next().find_next().text
    print(base_url)

    # 先寻找第一个table 然后下下个兄弟节点是我需要的
    table = html_soup.find_all(
        'table')[1]
    # print(table)

    # url参数
    url_param_p = table.find('td')
    url_param = url_param_p.text
    print(url_param)

    # header的table
    header_table = table.find_next_sibling().find_next()
    header = header_table.find('td').text + ':application/x-www-form-urlencoded'
    print(header)

    # 开始构建参数列表
    request_parameters = []  # 里面由几个json构成
    params_table_before = html_soup.title('请求参数')

    params_table = html_soup.find_all('table')[2]
    # print(params_table)

    # 里面的tbody
    t_body = params_table.find('tbody')
    # print(t_body)

    tr_list = t_body.find_all('tr')
    # print(tr_list)

    # 将tr节点五个一组封装为字典
    result = [{f: td.text.strip() for f, td in
               zip(['param_name', 'is_requirment', 'type', 'optional_range', 'description'], tr.find_all('td'))} for tr
              in tr_list]

    request_parameters = result

    print(request_parameters)

    # 找到返回说明
    return_h2 = html_soup.find('h2', {"id": "返回说明"})
    return_table = return_h2.find_next_sibling().find_next_sibling()
    return_body = return_table.find('tbody')
    # 选tr节点
    tr_list1 = return_body.find_all('tr')
    # 将tr节点四个一组封装为字典
    result1 = [{f: td.text.strip() for f, td in
                zip(['param_name', 'is_requirment', 'type', 'description'], tr.find_all('td'))} for tr
               in tr_list1]

    response_parameters = result1
    print(response_parameters)

    # 返回实例 首先找到这个类
    return_example_div = html_soup.find('code', class_='language-json')

    # 获取code标签中的JSON字符串
    json_str = return_example_div.text

    dick = json.dumps(json_str, ensure_ascii=False, indent=4)

    return_example = dick
    print(return_example)

    # 组装
    api_list = []

    api_one = {"api_name": api_name, "api_description": api_description, "method": method, "base_url": base_url,
               "header": header, "url_param": url_param, "request_parameters": request_parameters,
               "response_parameters": response_parameters, "return_example": ""}


    api_one_json = json.dumps(api_one, ensure_ascii=False)

    # 打印格式化的JSON字符串

    print(api_one_json)


if __name__ == '__main__':
    get_html('https://ai.baidu.com/ai-doc/NLP/vk6z52h5n')
