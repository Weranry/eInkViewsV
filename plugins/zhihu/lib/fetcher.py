import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from modules.errors.errors import ParamError
import warnings

# 忽略 HTML 解析 XML 的警告
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def fetch_zhihu_daily():
    url = 'https://rsshub.umi.im/zhihu/daily'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 强制设置编码，防止部分环境解析 RSS 时文字乱码
        response.encoding = 'utf-8'
        xml_data = response.text

        # 优先使用 html.parser 以保证通用性，同时捕获 item/entry
        soup = BeautifulSoup(xml_data, 'html.parser')
        
        # 查找条目 (RSS 使用 item, Atom 使用 entry)
        item = soup.find('item') or soup.find('entry')
        
        if not item:
            raise ParamError("No zhihu daily items found in the response")

        title = item.find('title').get_text(strip=True) if item.find('title') else "No Title"
        
        # 处理链接: 
        # 在 html.parser 下，XML 的 <link>url</link> 可能被解析为 <link/> 且 url 变成 next_sibling
        link_tag = item.find('link')
        link = ""
        if link_tag:
            link = link_tag.get_text(strip=True)
            if not link:
                # 尝试获取 next_sibling (针对 html.parser 误判自闭合的情况)
                sibling = link_tag.next_sibling
                if sibling and isinstance(sibling, str):
                    link = sibling.strip()
                elif link_tag.get('href'):
                    link = link_tag.get('href')

        if not link:
            # 最后的保底手段：正则表达式提取
            import re
            link_match = re.search(r'<link>(.*?)</link>', xml_data, re.DOTALL | re.IGNORECASE)
            if link_match:
                link = link_match.group(1).strip()

        if not link:
            raise ParamError("Could not extract link from Zhihu daily item")

        # 确保链接是完整的 URL
        if not link.startswith('http'):
            # 如果是相对路径 (可能性较小)，补全
            pass

        return {
            "title": title,
            "link": link
        }
    except Exception as e:
        raise ParamError(f"Error fetching Zhihu daily: {str(e)}")
