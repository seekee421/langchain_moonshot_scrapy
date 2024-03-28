# 引入需要的库
import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from crawlbase import CrawlingAPI, ScraperAPI, LeadsAPI, ScreenshotsAPI, StorageAPI
from moonshot_model_test import ask_question
from url_get import bing_search

if __name__ == '__main__':
    # 获取./data/目录下的所有xlsx文件
    xlsx_files = [f for f in os.listdir('./data/') if f.endswith('.xlsx')]
    # 创建一个空字典，用于存储所有文件的第一列的数据
    data_dict = {}
    # 遍历所有xlsx文件
    for file in xlsx_files:
        # 读取Excel文件
        df = pd.read_excel('./data/' + file)
        # 遍历第一列的数据
        for index, row in df.iterrows():
            data_dict[file + '_' + str(index)] = row['标题']
    # 将data_dict中的键值存储为一个keyword_dict元组
    keyword_dict = list(data_dict.values())

# 通过Bing搜索引擎搜索关键词并获取前十篇相关网页的URL


if __name__ == '__main__':
    # 初始化一个空字典用于存储关键词和对应的URL列表
    url_dict = {}
    # 遍历keyword_dict列表
    for keyword in keyword_dict:
        # 更新url_dict字典
        url_dict[keyword] = bing_search(keyword)       
print(url_dict)

# 用crawlbase爬取URL的网页内容
# 初始化 CrawlingAPI 类
api = CrawlingAPI({'token': '1HQVJE9gEmDoJHo_F5oWvQ'})
# 初始化一个空字典用于存储网页内容
content_dict = {}
# 遍历 url_dict 中的每个条目
for title, urls in url_dict.items():
    content_list = []
    for url in urls:
        try:
            response = api.get(url)
            if response['status_code'] == 200:
                # 确认获取的是页面内容
                content = response.get('body', '')  # 或者 response['data']['content'] 根据实际情况调整
                content_list.append(content)
            else:
                print(f"Error fetching {url}: Status code {response['status_code']}")
        except Exception as e:
            print(f"Exception fetching {url}: {e}")
    content_dict[title] = content_list


if __name__ == '__main__':
    print(content_dict)

# processed_content_dict = {}  # 初始化一个新的字典来存储处理后的文本

# for title, content in content_dict.items():
#     processed_content = ask_question("请总结文本的关键信息", "content")  # 调用 ask_question 函数处理文本
#     processed_content_dict[title] = processed_content
    
# if __name__ == '__main__':
#     print(processed_content_dict)

