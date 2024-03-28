from crawlbase import CrawlingAPI
import re

api = CrawlingAPI({'token': '1HQVJE9gEmDoJHo_F5oWvQ'})

response = api.get('https://www.cqstl.gov.cn/bm/qfzggw_71098/zwgk_70831/fdzdgknr_70834/xzxk/bljg/202302/t20230217_11617448.html')
if response['status_code'] == 200:
    content = response['body']
    if isinstance(content, bytes):
        charset = 'utf-8'  # 默认编码
        if 'Content-Type' in response['headers']:
            content_type = response['headers']['Content-Type']
            if 'charset=' in content_type:
                charset = content_type.split('charset=')[-1]
        content = content.decode(charset, errors='ignore')
    
    # 使用正则表达式提取中文文本
    chinese_text = re.findall(r'[\u4e00-\u9fa5]+', content)
    print(' '.join(chinese_text))