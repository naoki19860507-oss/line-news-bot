import os
import feedparser
from datetime import datetime, timezone, timedelta
import requests

# ===== 設定 =====
# 各サイトの正式名と、Google Newsの検索対象ドメイン
SOURCES = [
    ("日経新聞", "nikkei.com"),
    ("NewsPicks", "newspicks.com"),
    ("ビジネスインサイダー", "businessinsider.jp"),
    ("Yahoo!ニュース", "news.yahoo.co.jp"),
    ("ITmedia", "itmedia.co.jp"),
]

ARTICLES_PER_SOURCE = 3          # 1サイトあたりの記事数
LINE_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"


def fetch_articles(domain, limit=ARTICLES_PER_SOURCE):
    """Google News RSS経由で、指定ドメインの最新記事を取得する"""
    url = f"https://news.google.com/rss/search?q=site:{domain}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:limit]:
        title = entry.title
        link = entry.link
        articles.append((title, link))
    return articles


def build_message():
    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).strftime("%m/%d(%a)")
    lines = [f"📰 {today} 朝のニュースまとめ\n"]

    for name, domain in SOURCES:
        lines.append(f"■ {name}")
        try:
            articles = fetch_articles(domain)
            if not articles:
                lines.append("（記事が取得できませんでした）")
            for title, link in articles:
                lines.append(f"・{title}\n{link}")
        except Exception as e:
            lines.append(f"（取得エラー: {e}）")
        lines.append("")  # 空行区切り

    return "\n".join(lines).strip()


def send_line_message(text):
    # LINEの1メッセージは5000文字制限。超える場合は分割する
    chunks = [text[i:i + 4900] for i in range(0, len(text), 4900)] or [text]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    }
    for chunk in chunks:
        payload = {
            "to": LINE_USER_ID,
            "messages": [{"type": "text", "text": chunk}],
        }
        res = requests.post(LINE_PUSH_URL, headers=headers, json=payload)
        if res.status_code != 200:
            raise RuntimeError(f"LINE送信失敗: {res.status_code} {res.text}")


if __name__ == "__main__":
    message = build_message()
    send_line_message(message)
    print("送信完了")
    print(message)
