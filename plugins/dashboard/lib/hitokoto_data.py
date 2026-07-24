import requests
import traceback


def fetch_hitokoto():
    try:
        resp = requests.get("https://v1.hitokoto.cn/", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "text": data.get("hitokoto", ""),
            "source": data.get("from", ""),
            "author": data.get("from_who", ""),
        }
    except Exception:
        print("一言 API 获取失败")
        traceback.print_exc()
        return {
            "text": "生活不止眼前的苟且，还有诗和远方。",
            "source": "备用",
            "author": "",
        }