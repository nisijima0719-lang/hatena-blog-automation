# はてなブログ自動投稿システム セットアップガイド

トレンド情報を取り込んだ自動記事生成 + 2～3日ごとの自動投稿システム

---

## 📋 必要な情報

### 1. はてなブログ認証情報
- **はてなID**: `kuchanclaude0220`
- **ブログID群**: 
  - `kuchanclaude0220` (藤原 健人)
  - `rakuten-mobile-1500yen` (星野 翔太)
  - `nurse-beauty-health` (鈴木 美咲)
- **AtomPub APIキー**: `szdrhb2agm` （共通）

### 2. Anthropic API キー
- https://console.anthropic.com で取得
- 形式: `sk-ant-xxxxxxxxxxxxx`

### 3. GitHub リポジトリ
- このプロジェクトをGitHubにPush
- Settings → Secrets and variables → Actions で環境変数を設定

---

## 🚀 セットアップ手順

### ステップ1: ローカル環境構築

```bash
cd ~/hatena-blog-automation

# 依存パッケージをインストール
pip install -r requirements.txt

# 環境変数ファイルを作成
cp .env.example .env

# .env を編集（各APIキーを入力）
nano .env
```

### ステップ2: 環境変数の設定内容

`.env` ファイルに以下を記入：

```
HATENA_ID=kuchanclaude0220
HATENA_API_KEY=szdrhb2agm
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxx
```

### ステップ3: ローカルテスト

```bash
# キャラクターを指定して実行（テスト用）
python scripts/generate_and_post.py kento

# または、ランダムに選択
python scripts/generate_and_post.py
```

### ステップ4: GitHubにPush

```bash
# リポジトリを初期化（まだならば）
git init
git add .
git commit -m "Initial commit: Hatena blog automation system"

# リモートにPush
git remote add origin https://github.com/{YOUR_USERNAME}/{REPO_NAME}.git
git branch -M main
git push -u origin main
```

### ステップ5: GitHub Secrets設定

1. GitHub リポジトリを開く
2. **Settings** → **Secrets and variables** → **Actions**
3. 以下の3つを追加：

| 名前 | 値 |
|---|---|
| `HATENA_ID` | `kuchanclaude0220` |
| `HATENA_API_KEY` | `szdrhb2agm` |
| `ANTHROPIC_API_KEY` | `sk-ant-xxxxx...` |

### ステップ6: GitHub Actions の有効化

1. **Actions** タブを開く
2. ワークフロー `Auto Blog Post` が表示されることを確認
3. **Enable workflow** をクリック（必要に応じて）

---

## 📅 投稿スケジュール

### 現在の設定
- **毎日 09:00 JST** - キャラクター①（藤原 健人）
- **毎日 13:00 JST** - キャラクター②（星野 翔太）
- **毎日 18:00 JST** - キャラクター③（鈴木 美咲）

→ **結果的に 2～3日ごと** に各キャラクターが投稿される

### カスタマイズ方法

`.github/workflows/auto-post.yml` の `cron` 設定を変更：

```yaml
schedule:
  - cron: '0 9 * * 1,4'    # 月・木の 18:00 JST
  - cron: '0 18 * * 2,5'   # 火・金の 03:00 JST（翌朝）
```

**Cron形式:** `分 時間 日 月 曜日`

---

## 🧪 トラブルシューティング

### エラー: "Failed to extract JSON from response"
→ Claude APIレスポンスの形式が変わっている可能性
→ `scripts/generate_and_post.py` のプロンプトを調整

### エラー: "Failed to post (Status 401)"
→ はてなID / APIキーが間違っている
→ GitHub Secrets を確認

### エラー: "ANTHROPIC_API_KEY not set"
→ `.env` ファイルが `.gitignore` に入っていることを確認
→ GitHub Actions では Secrets から自動で読み込まれます

### 記事が公開されない
→ `.github/workflows/auto-post.yml` で `app:draft` が `yes` になっていないか確認
→ 現在は `no`（公開）に設定

---

## 📊 実行ログ確認

GitHub Actions の実行ログを確認：

1. リポジトリ → **Actions** タブ
2. **Auto Blog Post** ワークフロー
3. 最新の Run をクリック
4. Job の出力を確認

---

## 🔧 カスタマイズ例

### トレンド情報の改善

`scripts/generate_and_post.py` の `get_trending_topics()` 関数を拡張：

```python
def get_trending_topics(character_key: str) -> str:
    # Google Trends API / News API を使用
    # 実装例を追加
    pass
```

### 記事の自動化レベルを上げる

- Twitter/X のトレンド自動取得
- Reddit からのトピック抽出
- Yahoo! ニュース RSS の取り込み

---

## ⚙️ 推奨設定

### 実行間隔のバランス

**問題:** 毎日3人が投稿されると投稿頻度が高い
**解決案:** スケジュールを調整

```yaml
# 案A：週1回ずつ
schedule:
  - cron: '0 9 * * 1'     # 月曜 18:00
  - cron: '0 9 * * 3'     # 水曜 18:00
  - cron: '0 9 * * 5'     # 金曜 18:00
```

```yaml
# 案B：2日ごと
schedule:
  - cron: '0 9 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31 * *'
```

---

## 📝 ローカルで記事をドラフト保存する（公開前確認）

`scripts/generate_and_post.py` を実行時に以下の環境変数を設定：

```bash
DRAFT_ONLY=true python scripts/generate_and_post.py kento
```

記事を JSON ファイルとして `/tmp/draft_{character}_{timestamp}.json` に保存

---

## 🔒 セキュリティ注意事項

- **API キーは絶対にGitにコミットしない** → `.gitignore` で管理
- GitHub Secrets に保存（Gitには表示されない）
- `.env` は `.gitignore` に含める
- 定期的にAPIキーをローテーション

---

## 📞 サポート

問題が発生した場合：

1. GitHub Actions のログを確認
2. ローカルでテスト実行
3. `scripts/generate_and_post.py` を直接実行してエラーを確認

```bash
# デバッグモード
python -u scripts/generate_and_post.py kento 2>&1
```

---

**セットアップ完了！自動ブログ運用を開始してください。** 🎉
