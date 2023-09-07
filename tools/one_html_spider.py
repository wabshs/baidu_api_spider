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
    table = html_soup.find(
        'table')
    # print(table)

    # url参数
    url_param_p = table.find('td')
    url_param = url_param_p.text
    print(url_param)

    # header的table
    header_table = table.find_next_sibling().find_next()
    header = header_table.find('td').text
    print(header)

    # 开始构建参数列表
    request_parameters = []  # 里面由几个json构成
    params_table = table.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
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

    # 化成json
    result_json = json.dumps(result,ensure_ascii=False)

    request_parameters = result_json

    print(result_json)

    # print(result)

    # # 构建json
    # api_list = {}
    # data = json.loads(json.dumps(api_list))
    #
    # data['api_name'] = api_name
    # data['api_description'] = api_description
    # data['method'] = method
    # data['base_url'] = base_url
    #
    # api_list_json = json.dumps(data,ensure_ascii=False)
    #
    # print(api_list_json)


if __name__ == '__main__':
    get_html('https://ai.baidu.com/ai-doc/OCR/1k3h7y3db')
