import requests
from bs4 import BeautifulSoup
import json


def get_html(url: str):
    # 转化为bs对象
    html_response = requests.get(url)
    html = html_response.text
    html_soup = BeautifulSoup(html, 'html.parser')

    # api_name
    if html_soup.find('h1', class_='post__title'):
        api_name = html_soup.find('h1', class_='post__title').text

    # 接口描述
    api_description = None
    if html_soup.find(id="接口描述"):
        api_description = html_soup.find(id="接口描述").find_next_sibling().text

    # method
    if html_soup.find('code', class_='language-text'):
        method = html_soup.find('code', class_='language-text').text

    # base_url
    base_url = html_soup.find_all('code', class_='language-text')[1].text

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

    tr_list = t_body.find_all('tr')

    # 将tr节点4个一组封装为字典
    result = [{f: td.text.strip() for f, td in
               zip(['param_name', 'is_requirement', 'type', 'range', 'description'], tr.find_all('td'))} for tr
              in tr_list]

    request_parameters = result

    # 返回参数
    if html_soup.find(id="返回参数"):
        return_p_table = html_soup.find(id="返回参数").find_next_sibling()
    elif html_soup.find('p', string="返回参数"):
        return_p_table = html_soup.find('p', string="返回参数").find_next_sibling()
    else:
        return_p_table = html_soup.find('strong', string="返回参数").find_next_sibling()

    # 里面的tbody
    t_body = return_p_table.find('tbody')

    tr_list = t_body.find_all('tr')

    # 将tr节点3个一组封装为字典
    result = [{f: td.text.strip() for f, td in
               zip(['param_name', 'is_requirement', 'type', 'description'], tr.find_all('td'))} for tr
              in tr_list]

    response_parameters = result

    # 组装
    api_one = {"api_name": api_name, "api_description": api_description, "method": method, "base_url": base_url,
               "header": header, "url_param": url_param, "request_parameters": request_parameters,
               "response_parameters": response_parameters, "return_example": ""}

    api_one_json = json.dumps(api_one, ensure_ascii=False)
    print(api_one_json + ",")


if __name__ == '__main__':
    api_url = [{'category_name': '文字识别', 'api_category_name': '教育场景文字识别', 'api_name': '试卷分析与识别',
                'api_url': 'https://ai.baidu.com/ai-doc/OCR/jk9m7mj1l'},
               {'category_name': '文字识别', 'api_category_name': '教育场景文字识别', 'api_name': '公式识别',
                'api_url': 'https://ai.baidu.com/ai-doc/OCR/Ok3h7xxva'},
               {'category_name': '文字识别', 'api_category_name': '教育场景文字识别', 'api_name': '词典笔文字识别',
                'api_url': 'https://ai.baidu.com/ai-doc/OCR/8li88kqoh'}]
    html_content_list = []
    for api in api_url:
        url = api['api_url']
        get_html(url)
