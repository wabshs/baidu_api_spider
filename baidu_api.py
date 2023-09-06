import tools.get_api_category_links
import tools.parse_api_information
import tools.get_category_doc_links

base_url = 'https://ai.baidu.com/ai-doc'

print('OCR的地址:============================')

links_all = tools.get_category_doc_links.get_category_links(base_url)

# 提取OCR这个大类
OCR_list = [element for element in links_all if element.startswith('https://ai.baidu.com/ai-doc/OCR')]
# 打印OCR所有的Api地址
print(OCR_list)

