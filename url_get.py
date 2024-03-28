#使用bing搜索引擎搜索关键词并获取前十篇相关网页的URL
import requests
from bs4 import BeautifulSoup

def bing_search(keyword):
    # Bing 搜索 URL
    base_url = 'https://www.bing.com'
    search_url = f'{base_url}/search?q={keyword}'

    # 发送搜索请求
    response = requests.get(search_url)
    response.raise_for_status()  # 确保请求成功

    # 解析返回的 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找包含搜索结果的元素，这里使用的选择器可能需要根据实际页面结构调整
    results = soup.find_all('li', class_='b_algo', limit=10)

    # 提取并打印 URL
    urls = []
    for result in results:
        link = result.find('a')
        if link and link['href']:
            urls.append(link['href'])

    return urls

# # 测试函数
# if __name__ == '__main__':
#     keyword = 'Python'
#     urls = bing_search(keyword)
#     for url in urls:
#         print(url)
