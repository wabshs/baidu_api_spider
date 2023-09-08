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
               zip(['param_name', 'is_requirement', 'type', 'between', 'description'], tr.find_all('td'))} for tr
              in tr_list]

    request_parameters = result

    # 返回参数
    if html_soup.find(id="返回参数"):
        return_p_table = html_soup.find(id="返回参数").find_next_sibling()
    else:
        return_p_table = html_soup.find('strong', string="返回参数").parent.find_next_sibling()

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
    api_url = [
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '身份证识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/rk3h7xzck'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '身份证混贴识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/akp3gfbmc'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '身份证识别（金融加密版）',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/Akkpbt2j4'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '银行卡识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/ak3h7xxg3'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '营业执照识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/sk3h7y3zs'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '护照识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/Wk3h7y1gi'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '社保卡识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/lkto93055'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '户口本识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/ak3h7xzk7'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '出生医学证明识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/mk3h7y1o6'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '企业工商信息查询（标准版）',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/Zl9nxwzhn'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '企业工商信息查询（高级版）',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/il9nybi81'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '企业三要素核验',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/Ol9nyzwa2'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '企业四要素核验',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/7l9nz69kp'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '港澳台证件识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/Tlg6859ns'},
        {'category_name': '文字识别', 'api_category_name': '卡证文字识别', 'api_name': '结婚证识别',
         'api_url': 'https://ai.baidu.com/ai-doc/OCR/Klg67mfkc'}]
    html_content_list = []
    for api in api_url:
        url = api['api_url']
        get_html(url)
