from typing import List

import requests
from bs4 import BeautifulSoup


def get_category_links(url: str) -> List[str]:
    """
    获取所有的api-doc地址保存到target_doc_links列表中
    :param url:
    :return:
    """
    # url = 'https://ai.baidu.com/ai-doc'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('div', class_='ai-product-content-multiple-children')
    category_doc_links = []
    for block in data:
        ai_product_content_multiple_links = block.find_all('div', {'class': 'ai-product-content-multiple-links'})
        for ai_product_content_multiple_link in ai_product_content_multiple_links:
            a_tag = ai_product_content_multiple_link.find('a')
            if a_tag is not None:
                link = a_tag.get('href')
                if 'http' not in link:
                    link = 'https://ai.baidu.com' + link
                category_doc_links.append(link)
    return category_doc_links
