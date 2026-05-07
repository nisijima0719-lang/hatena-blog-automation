# 🚀 はてなブログ自動投稿システム

トレンド情報を自動取得して、3つのキャラクターが 2～3日ごとに記事を自動生成・投稿するシステムです。

```
トレンド取得 → Claude APIで記事生成 → はてなブログに自動投稿
```

---

## 📋 システム概要

### 3つのブログ・キャラクター

| キャラ | ブログテーマ | 主要案件 | 単価 |
|---|---|---|---|
| **藤原 健人** | AI × 資産形成 | 楽天証券 | 🔴 高 |
| **星野 翔太** | 通信費削減 | 楽天モバイル | 🟡 中 |
| **鈴木 美咲** | 美容×健康 | サプリメント | 🟢 中 |

---

## ✨ 機能

- ✅ **自動記事生成** - Claude APIでトレンドを組み込んだ記事を毎回新規生成
- ✅ **キャラクター別カスタマイズ** - 各キャラの口調・専門分野に合わせた記事
- ✅ **定期自動投稿** - GitHub Actions で 2～3日ごとに投稿
- ✅ **トレンド対応** - 常に最新情報を反映した記事
- ✅ **複数ブログ管理** - 1つのシステムで3つのブログを同時運用

---

## 🏗️ プロジェクト構造

```
hatena-blog-automation/
├── .github/workflows/
│   └── auto-post.yml              # GitHub Actions ワークフロー
├── scripts/
│   └── generate_and_post.py       # メインの記事生成・投稿スクリプト
├── characters/
│   ├── kento_ai_investment.md     # 藤原 健人 の設定
│   ├── shota_mobile_saving.md     # 星野 翔太 の設定
│   └── misaki_beauty_health.md    # 鈴木 美咲 の設定
├── .env.example                   # 環境変数テンプレート
├── requirements.txt               # Python依存パッケージ
├── SETUP.md                       # セットアップガイド
└── README.md                      # このファイル
```

---

## 🚀 クイックスタート

### 1. セットアップ
```bash
cd ~/hatena-blog-automation
cp .env.example .env
# .env を編集してAPIキーを入力
nano .env
```

### 2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

### 3. ローカルテスト
```bash
python scripts/generate_and_post.py kento
```

### 4. GitHubにPush & GitHub Secrets設定
```bash
git push origin main
```

GitHub Settings → Secrets に `HATENA_ID`, `HATENA_API_KEY`, `ANTHROPIC_API_KEY` を登録

### 5. 自動投稿開始！
→ GitHub Actions が毎日スケジュール通りに実行開始

---

## 📅 投稿スケジュール

現在：
- **毎日 09:00 JST** - 藤原 健人
- **毎日 13:00 JST** - 星野 翔太  
- **毎日 18:00 JST** - 鈴木 美咲

**結果：** 各キャラが 2～3日ごとに投稿される

カスタマイズは `SETUP.md` を参照

---

## 🎯 記事の特徴

### 自動生成される記事
- **長さ** 1,500～2,000文字
- **スタイル** キャラクターの口調・専門分野に合わせた
- **トレンド** 最新情報・季節ネタを自動組み込み
- **アフィリエイト** 各キャラの専門案件へ自然な導線

### 例：藤原 健人（AI投資）
```
タイトル: 「ChatGPT×楽天証券で投資を自動化した話」

本文:
- AI自動化トレンド
- 楽天証券の最新キャンペーン
- 実際の運用実績
- 楽天カード・銀行への導線
```

---

## 🔧 カスタマイズ

### 記事生成プロンプトを変更
`scripts/generate_and_post.py` の `generate_article()` 関数内の `prompt` 変数を編集

### キャラクター設定を編集
`characters/*.md` ファイルを編集して口調や専門分野を変更

### 投稿スケジュールを変更
`.github/workflows/auto-post.yml` の `cron` を編集

詳細は `SETUP.md` 参照

---

## 📊 実行ログ確認

GitHub Actions の実行状況を確認：

1. GitHub リポジトリ → **Actions** タブ
2. **Auto Blog Post** ワークフロー
3. 最新の Run をクリック
4. ジョブの実行ログを確認

---

## 🔒 セキュリティ

- API キーは `.env` で管理（Git にはコミットしない）
- GitHub Secrets に保存（Workflows から自動取得）
- `.gitignore` に `.env` を含める

---

## 📝 トラブルシューティング

### よくある問題

**Q: 記事が投稿されない**
- A: GitHub Secrets に正しいAPIキーが設定されているか確認

**Q: 生成される記事の質が低い**
- A: `characters/*.md` のプロンプト要素を詳しく記述

**Q: トレンド情報が反映されていない**
- A: `get_trending_topics()` 関数を Web API 連携で拡張

詳細は `SETUP.md` のトラブルシューティング参照

---

## 📈 今後の拡張案

- [ ] Google Trends API 連携（自動トレンド取得）
- [ ] ニュースAPI・RSS フィード統合
- [ ] Slack 通知機能
- [ ] 記事パフォーマンス追跡（アクセス数・クリック率）
- [ ] SNS 自動連携（Twitter/X、Facebook）
- [ ] AIで記事の良い点・改善点を自動分析

---

## 📞 サポート・フィードバック

問題が発生した場合：

1. `SETUP.md` のトラブルシューティング確認
2. ローカルで `python scripts/generate_and_post.py kento` でテスト
3. GitHub Issues で報告

---

**Happy blogging! 🎉**
