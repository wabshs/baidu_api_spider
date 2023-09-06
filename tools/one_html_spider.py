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

    # 构建json
    api_list = {}
    data = json.loads(json.dumps(api_list))

    data['api_name'] = api_name
    data['api_description'] = api_description
    data['method'] = method
    data['base_url'] = base_url

    api_list_json = json.dumps(data,ensure_ascii=False)

    print(api_list_json)


if __name__ == '__main__':
    get_html('https://ai.baidu.com/ai-doc/OCR/1k3h7y3db')
