import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from modules.errors.errors import ParamError

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


def fetch_news(max_items=12):
    all_items = []

    for src in RSS_SOURCES:
        try:
            resp = requests.get(src["url"], timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (compatible; eInkViews/1.0)"
            })
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            items = _parse_rss_feed(resp.text, src["name"])
            all_items.extend(items)
        except (requests.exceptions.Timeout, requests.exceptions.RequestException):
            continue
        except ET.ParseError:
            continue

    if not all_items:
        raise ParamError("无法获取新闻数据，所有 RSS 源均不可用")

    all_items.sort(key=lambda x: x.get("pub_date", ""), reverse=True)

    return all_items[:max_items]