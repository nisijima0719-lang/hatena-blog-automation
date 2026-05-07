#!/usr/bin/env python3
"""
トレンド情報を取得 → 記事自動生成 → はてなブログに投稿
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import requests
from anthropic import Anthropic

# 設定
HATENA_ID = os.getenv("HATENA_ID")
HATENA_API_KEY = os.getenv("HATENA_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

CHARACTERS = {
    "kento": {
        "name": "藤原 健人",
        "blog_id": "kuchanclaude0220",
        "config_path": "../characters/kento_ai_investment.md"
    },
    "shota": {
        "name": "星野 翔太",
        "blog_id": "rakuten-mobile-1500yen",
        "config_path": "../characters/shota_mobile_saving.md"
    },
    "misaki": {
        "name": "鈴木 美咲",
        "blog_id": "nurse-beauty-health",
        "config_path": "../characters/misaki_beauty_health.md"
    }
}


def load_character_config(character_key: str) -> str:
    """キャラクター設定ファイルを読み込み"""
    config_path = Path(__file__).parent / CHARACTERS[character_key]["config_path"]
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_trending_topics(character_key: str) -> str:
    """トレンド情報を取得（Google Trends, ニュースAPI等）"""
    # 簡易版：キャラクターごとの検索キーワードを定義
    trending_keywords = {
        "kento": ["AI", "ChatGPT", "Claude", "楽天証券", "NISA", "家計管理"],
        "shota": ["楽天モバイル", "格安SIM", "キャリア", "通信費", "ソフトバンク", "au"],
        "misaki": ["美容トレンド", "スキンケア", "サプリメント", "ボディメイク", "季節美容"]
    }

    keywords = trending_keywords.get(character_key, [])
    # 実装例：WebSearchAPIやGoogle Trends APIを使用
    # ここではダミーデータを返す（本番環境では実際のAPI連携が必要）

    today = datetime.now().strftime("%Y年%m月%d日")
    trend_text = f"【{today}のトレンド情報】\n"
    trend_text += f"注目キーワード: {', '.join(keywords[:3])}\n"

    return trend_text


def generate_article(character_key: str, trending_info: str) -> dict:
    """Claude APIを使って記事を生成"""

    character_config = load_character_config(character_key)

    prompt = f"""{character_config}

## トレンド情報
{trending_info}

## 指示
上記のキャラクター設定とトレンド情報を基に、ブログ記事を生成してください。

以下の形式で出力してください：
```json
{{
    "title": "記事のタイトル（SEOを考慮、40-60字）",
    "body": "本文（1500-2000字。Markdown形式。段落は\\n\\nで区切る）",
    "tags": ["タグ1", "タグ2", "タグ3"]
}}
```

### 要件
- キャラクターの口調・スタイルを厳密に守る
- トレンド情報を自然に組み込む
- アフィリエイトリンク導線を自然に作る
- 最後に「\\n\\n---\\n\\n**本記事について**: このブログは〇〇についての個人的な体験と情報を共有しています。」という免責事項を追加
- 見出し(##, ###)を適切に使用して読みやすくする
"""

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    print(f"🤖 Generating article for {CHARACTERS[character_key]['name']}...")

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2500,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = message.content[0].text

    # JSONを抽出
    json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if not json_match:
        print("❌ Failed to extract JSON from response")
        print(response_text)
        sys.exit(1)

    article_data = json.loads(json_match.group(1))

    return article_data


def post_to_hatena(character_key: str, article_data: dict) -> bool:
    """はてなブログのAtomPub APIで記事を投稿"""

    blog_id = CHARACTERS[character_key]["blog_id"]

    # AtomPub API URL
    url = f"https://blog.hatena.ne.jp/{HATENA_ID}/{blog_id}/atom/entry"

    # Atom Entry形式でXMLを構築
    entry = ET.Element("entry")
    entry.set("xmlns", "http://www.w3.org/2005/Atom")

    title = ET.SubElement(entry, "title")
    title.text = article_data["title"]

    content = ET.SubElement(entry, "content")
    content.set("type", "text/html")
    content.text = article_data["body"]

    # タグ
    for tag in article_data.get("tags", []):
        category = ET.SubElement(entry, "category")
        category.set("term", tag)

    # ステータス（draft: 下書き, publish: 公開）
    draft = ET.SubElement(entry, "app:control")
    draft.set("xmlns:app", "http://www.w3.org/2007/app")
    draft_elem = ET.SubElement(draft, "app:draft")
    draft_elem.text = "no"  # 公開

    # XMLを文字列に
    xml_string = ET.tostring(entry, encoding='unicode')

    # リクエスト送信
    headers = {
        "Authorization": f"Basic {_get_basic_auth(HATENA_ID, HATENA_API_KEY)}",
        "Content-Type": "application/atom+xml"
    }

    try:
        response = requests.post(url, data=xml_string.encode('utf-8'), headers=headers)

        if response.status_code in [200, 201]:
            print(f"✅ Posted successfully: {blog_id}")
            return True
        else:
            print(f"❌ Failed to post (Status {response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error posting to Hatena: {e}")
        return False


def _get_basic_auth(user_id: str, api_key: str) -> str:
    """Basic認証の値を生成"""
    import base64
    credentials = f"{user_id}:{api_key}"
    return base64.b64encode(credentials.encode()).decode()


def main(character_key: str = None):
    """メイン処理"""

    # 環境変数チェック
    if not all([HATENA_ID, HATENA_API_KEY, ANTHROPIC_API_KEY]):
        print("❌ Required environment variables not set:")
        print(f"   HATENA_ID: {bool(HATENA_ID)}")
        print(f"   HATENA_API_KEY: {bool(HATENA_API_KEY)}")
        print(f"   ANTHROPIC_API_KEY: {bool(ANTHROPIC_API_KEY)}")
        sys.exit(1)

    # キャラクター選択（指定がなければランダム）
    if not character_key:
        import random
        character_key = random.choice(list(CHARACTERS.keys()))

    if character_key not in CHARACTERS:
        print(f"❌ Unknown character: {character_key}")
        print(f"   Available: {list(CHARACTERS.keys())}")
        sys.exit(1)

    print(f"\n📝 Starting article generation for: {CHARACTERS[character_key]['name']}")

    # ステップ1: トレンド情報取得
    print("📊 Fetching trending topics...")
    trending_info = get_trending_topics(character_key)
    print(trending_info)

    # ステップ2: 記事生成
    article_data = generate_article(character_key, trending_info)
    print(f"\n📄 Generated article:")
    print(f"   Title: {article_data['title']}")
    print(f"   Length: {len(article_data['body'])} characters")

    # ステップ3: はてなブログに投稿
    print("\n🚀 Posting to Hatena Blog...")
    success = post_to_hatena(character_key, article_data)

    if success:
        print(f"\n✨ All done! Article posted successfully.")
    else:
        print(f"\n⚠️ Article generated but failed to post.")

    return success


if __name__ == "__main__":
    character_key = sys.argv[1] if len(sys.argv) > 1 else None
    success = main(character_key)
    sys.exit(0 if success else 1)
