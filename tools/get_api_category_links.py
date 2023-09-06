from typing import List

import requests
from bs4 import BeautifulSoup


def get_api_links(category_doc_links: List[str]) -> List[str]:
    """
    解析api-doc
    :param category_doc_links:
    :return:
    """
    api_category_list = []
    for api_doc_link in category_doc_links:
        link_response = requests.get(api_doc_link)
        link_html = link_response.text
        link_soup = BeautifulSoup(link_html, 'html.parser')
        title_link = link_soup.find_all('li', class_='level-2 menu-item')
        target_link = [link for link in title_link if 'api' in link.text.lower()]
        for ai_product_content_link in target_link:
            a_tag = ai_product_content_link.find('a')
            if a_tag is not None:
                link = "https://ai.baidu.com" + a_tag.get('href')
                api_category_list.append(link)
    return api_category_list
