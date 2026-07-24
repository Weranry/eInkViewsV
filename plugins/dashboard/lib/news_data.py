import requests
import xml.etree.ElementTree as ET

RSS_SOURCES = [
    {
        "name": "人民网",
        "url": "http://www.people.com.cn/rss/politics.xml",
    },
    {
        "name": "新华网",
        "url": "http://www.xinhuanet.com/politics/xhszyw.xml",
    },
    {
        "name": "环球网",
        "url": "https://www.huanqiu.com/rss/world.xml",
    },
]


def _strip_html(text):
    result = ""
    in_tag = False
    for ch in text:
        if ch == "<":
            in_tag = True
        elif ch == ">":
            in_tag = False
        elif not in_tag:
            result += ch
    result = " ".join(result.split())
    return result


def _parse_rss_feed(xml_text, source_name):
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    channel = root.find("channel")
    if channel is None:
        return items

    for item_el in channel.findall("item"):
        title_el = item_el.find("title")
        desc_el = item_el.find("description")
        link_el = item_el.find("link")
        date_el = item_el.find("pubDate")

        title = title_el.text.strip() if title_el is not None and title_el.text else ""
        description = desc_el.text.strip() if desc_el is not None and desc_el.text else ""
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        pub_date = date_el.text.strip() if date_el is not None and date_el.text else ""

        if not title:
            continue

        clean_desc = _strip_html(description) if description else ""
        if len(clean_desc) > 200:
            clean_desc = clean_desc[:200] + "..."

        items.append({
            "title": title,
            "summary": clean_desc,
            "link": link,
            "pub_date": pub_date,
            "source": source_name,
        })

    return items


def fetch_news(max_items=8):
    all_items = []

    for src in RSS_SOURCES:
        try:
            resp = requests.get(src["url"], timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (compatible; eInkViews/1.0)"
            })
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            items = _parse_rss_feed(resp.text, src["name"])
            if items:
                print("新闻 RSS [{}] 获取成功, {}条".format(src["name"], len(items)))
            all_items.extend(items)
        except requests.exceptions.Timeout:
            print("新闻 RSS [{}] 超时".format(src["name"]))
            continue
        except requests.exceptions.RequestException:
            print("新闻 RSS [{}] 请求失败".format(src["name"]))
            continue
        except ET.ParseError:
            print("新闻 RSS [{}] XML 解析失败".format(src["name"]))
            continue

    if not all_items:
        print("所有 RSS 源均不可用，使用备用新闻")
        return [
            {"title": "中国经济稳步复苏，二季度GDP增长超预期", "source": "备用", "pub_date": ""},
            {"title": "科技创新大会在京召开，多项成果发布", "source": "备用", "pub_date": ""},
            {"title": "全国多地迎来高温天气，请注意防暑降温", "source": "备用", "pub_date": ""},
            {"title": "外交部发言人回应近期国际热点问题", "source": "备用", "pub_date": ""},
            {"title": "2026年世界人工智能大会即将开幕", "source": "备用", "pub_date": ""},
            {"title": "新能源产业持续快速增长，装机容量创新高", "source": "备用", "pub_date": ""},
            {"title": "教育部发布新政策，推动素质教育改革", "source": "备用", "pub_date": ""},
            {"title": "国际体育赛事精彩纷呈，中国队再创佳绩", "source": "备用", "pub_date": ""},
        ]

    all_items.sort(key=lambda x: x.get("pub_date", ""), reverse=True)

    return all_items[:max_items]