import json
import requests
from bs4 import BeautifulSoup


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
        table = html_soup.find(id="请求参数").find_next_sibling()
    elif html_soup.find('p', string="请求参数"):
        table = html_soup.find('p', string="请求参数").find_next_sibling()
    else:
        table = html_soup.find('strong', string="请求参数").parent.find_next_sibling()
    # 提取表格字段名
    header_row = table.find('tr')
    field_names = [th.text.strip() for th in header_row.find_all('th')]

    # 提取表格数据行并为每一行创建对应的字典
    data_rows = table.find_all('tr')[1:]  # 跳过表头行
    result = []
    for row in data_rows:
        field_values = [td.text.strip() for td in row.find_all('td')]
        row_dict = dict(zip(field_names, field_values))
        result.append(row_dict)

    request_parameters = result

    # 返回参数
    if html_soup.find(id="返回参数"):
        return_p_table = html_soup.find(id="返回参数").find_next_sibling()
    elif html_soup.find('p', string="返回参数"):
        table = html_soup.find('p', string="返回参数").find_next_sibling()
    else:
        table = html_soup.find('strong', string="返回参数").parent.find_next_sibling()

        # 提取表格字段名
    header_row = table.find('tr')
    field_names = [th.text.strip() for th in header_row.find_all('th')]

    # 提取表格数据行并为每一行创建对应的字典
    data_rows = table.find_all('tr')[1:]  # 跳过表头行
    result = []
    for row in data_rows:
        field_values = [td.text.strip() for td in row.find_all('td')]
        row_dict = dict(zip(field_names, field_values))
        result.append(row_dict)

    response_parameters = result

    code_tags = html_soup.find_all('code', class_='language-text')

    # 检查是否至少找到一个 code 标签
    text_content = None
    # 组装
    api_one = {"api_name": api_name, "api_description": api_description, "method": method, "base_url": base_url,
               "header": header, "url_param": url_param, "request_parameters": request_parameters,
               "response_parameters": response_parameters, "return_example": text_content}

    api_one_json = json.dumps(api_one, ensure_ascii=False)

    print(api_one_json + ",")


if __name__ == '__main__':
    api_url = [
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '组合接口',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Kkbg3gxs7'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '图像识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Xk3bcxe21'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '图像单主体检测',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Xk3bcxdum'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '动物识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Zk3bcxdfr'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '植物识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Mk3bcxe9i'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': 'logo识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Ok3bcxc59'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '果蔬识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/wk3bcxevq'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '自定义菜品识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Sk3bcxcd0'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '菜品识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/tk3bcxbb0'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '红酒识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Tk3bcxctf'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '货币识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/pk3bcxavy'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '地标识别',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/jk3bcxbih'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '图像多主体检测',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Wk7em3moi'},
        {'category_name': '图像技术', 'api_category_name': '图像识别', 'api_name': '自定义红酒识别（邀测）',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGERECOGNITION/skh4k58o4'},
        {'category_name': '图像技术', 'api_category_name': '图像搜索', 'api_name': '相似图片搜索',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGESEARCH/3k3bczqz8'},
        {'category_name': '图像技术', 'api_category_name': '图像搜索', 'api_name': '相同图片搜索',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGESEARCH/Ck3bczreq'},
        {'category_name': '图像技术', 'api_category_name': '图像搜索', 'api_name': '商品图片搜索',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGESEARCH/Dk3bczrmj'},
        {'category_name': '图像技术', 'api_category_name': '图像搜索', 'api_name': '绘本图片搜索',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGESEARCH/uk7emw71x'},
        {'category_name': '图像技术', 'api_category_name': '图像搜索', 'api_name': '面料图片搜索',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGESEARCH/kl6xkl6kq'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '黑白图像上色',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/Bk3bclns3'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像风格转换',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/xk3bclo77'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '自定义图像风格',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/al50vf6bq'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '人像动漫化',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/Mk4i6olx5'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像去雾',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/8k3bclp1l'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像对比度增强',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/ek3bclnzn'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像无损放大',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/ok3bclnkg'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '拉伸图像恢复',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/Rk3bclp97'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像修复',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/ok3bclome'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像清晰度增强',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/5k4i6mzqk'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像色彩增强',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/Tk9l4kll7'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图片去摩尔纹',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/ql4wdlnc0'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '文档图片去底纹',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/Nl6os53ab'},
        {'category_name': '图像技术', 'api_category_name': '图像增强与特效', 'api_name': '图像去噪',
         'api_url': 'https://ai.baidu.com/ai-doc/IMAGEPROCESS/Tl78sby7g'},
        {'category_name': '图像技术', 'api_category_name': '车辆分析', 'api_name': '车型识别',
         'api_url': 'https://ai.baidu.com/ai-doc/VEHICLE/tk3hb3eiv'},
        {'category_name': '图像技术', 'api_category_name': '车辆分析', 'api_name': '车辆检测',
         'api_url': 'https://ai.baidu.com/ai-doc/VEHICLE/rk3hb3flg'},
        {'category_name': '图像技术', 'api_category_name': '车辆分析', 'api_name': '车辆外观损伤识别',
         'api_url': 'https://ai.baidu.com/ai-doc/VEHICLE/fk3hb3f5w'},
        {'category_name': '图像技术', 'api_category_name': '车辆分析', 'api_name': '车辆属性识别',
         'api_url': 'https://ai.baidu.com/ai-doc/VEHICLE/mk3hb3fde'}
    ]
    html_content_list = []
    for api in api_url:
        url = api['api_url']
        get_html(url)
