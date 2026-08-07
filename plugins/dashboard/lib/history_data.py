import requests
from datetime import datetime
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from modules.common_timezone import now_in_timezone


WIKI_URL = "https://zh.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"
WIKI_EN_URL = "https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"


def fetch_history_today(tz=None):
    today = now_in_timezone(tz)
    month = today.month
    day = today.day

    items = _try_wiki(WIKI_URL, month, day)
    if items:
        return items

    items = _try_wiki(WIKI_EN_URL, month, day)
    if items:
        return items

    return [
        "1969年 人类首次登月成功",
        "1899年 海明威诞生",
        "公元前776年 首届奥林匹克运动会开幕",
    ]


def _try_wiki(url_template, month, day):
    try:
        url = url_template.format(month=month, day=day)
        resp = requests.get(url, timeout=10,
                           headers={"User-Agent": "eInkViews/1.0 (https://github.com)"})
        resp.raise_for_status()
        data = resp.json()
        events = data.get("events", [])
        items = []
        for ev in events[:4]:
            year = ev.get("year", "")
            text = ev.get("text", "")
            if text:
                clean = _strip_html(text)
                if clean:
                    items.append("{}年 {}".format(year, clean))
        return items if items else None
    except Exception:
        return None


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
    if len(result) > 80:
        result = result[:80]
    return result