import requests
from bs4 import BeautifulSoup
import json


def get_html(url: str):
    # 转化为bs对象
    html_response = requests.get(url)
    html = html_response.text
    html_soup = BeautifulSoup(html, 'html.parser')

    # api_name
    api_name = html_soup.find('h1', class_='post__title').text
    print(api_name)

    # 接口描述
    one = html_soup.find(id="接口描述")
    api_description = one.find_next_sibling().text
    print(api_description)

    # method
    method_sp = html_soup.find('code', class_='language-text')
    method = method_sp.text
    print(method)

    # base_url
    base_url = html_soup.find_all('code', class_='language-text')[1].text
    print(base_url)

    # url参数
    url_param = "access_token"

    # header
    header = "Content-Type:application/json"

    # 请求参数
    if html_soup.find(id="请求参数"):
        r_p_table = html_soup.find(id="请求参数").find_next_sibling()
    else:
        r_p_table = html_soup.find('p', string="请求参数").find_next_sibling()
    # 里面的tbody
    t_body = r_p_table.find('tbody')
    # print(t_body)

    tr_list = t_body.find_all('tr')
    # print(tr_list)

    # 将tr节点4个一组封装为字典
    result = [{f: td.text.strip() for f, td in
               zip(['param_name', 'type', 'is_requirement', 'description','remark'], tr.find_all('td'))} for tr
              in tr_list]

    request_parameters = result

    print(request_parameters)

    # 返回参数

    if html_soup.find(id="返回参数"):
        r_p_table = html_soup.find(id="返回参数").find_next_sibling()
    elif html_soup.find('li',string="正常返回"):
        r_p_table = html_soup.find('p', string="返回参数").find_next_siblings()[1]
    else:
        r_p_table = html_soup.find('p', string="返回参数").find_next_sibling()
    print(r_p_table)
    # 里面的tbody
    t_body = r_p_table.find('tbody')
    # print(t_body)

    tr_list = t_body.find_all('tr')
    # print(tr_list)

    # 将tr节点3个一组封装为字典
    result = [{f: td.text.strip() for f, td in
               zip(['param_name', 'type', 'is_requirement','description','remark'], tr.find_all('td'))} for tr
              in tr_list]

    response_parameters = result
    print(response_parameters)

    # 组装
    api_list = []

    api_one = {"api_name": api_name, "api_description": api_description, "method": method, "base_url": base_url,
               "header": header, "url_param": url_param, "request_parameters": request_parameters,
               "response_parameters": response_parameters, "return_example": ""}

    api_one_json = json.dumps(api_one, ensure_ascii=False)

    # 打印格式化的JSON字符串

    print(api_one_json)


if __name__ == '__main__':
    get_html('https://ai.baidu.com/ai-doc/MT/4kqryjku9')
