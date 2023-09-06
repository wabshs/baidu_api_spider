import json

import requests
from bs4 import BeautifulSoup


def analyze_api(url: str):
    doc_response = requests.get("https://ai.baidu.com/ai-doc/SPEECH/Jlbxdezuf")
    doc_html = doc_response.text
    doc_soup = BeautifulSoup(doc_html, 'html.parser')
    # ����ҳ��Ԫ��
    title_link = doc_soup.find_all(text="")
    # д�ļ�
    with open('data.json', 'w') as f:
        json.dump("data", f)
