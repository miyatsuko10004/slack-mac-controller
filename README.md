# Slack Mac Controller

スマホ（Slack）から自宅のMacの環境で `gemini` CLIを実行し、ローカル環境でAIからの回答を受け取るためのツールです。
SlackのSocket Modeを利用するため、Macのポート開放なしでセキュアに通信できます。

## 概要

Slack上でBot宛てにメンション付きでメッセージを送ると、その内容がそのままプロンプトとしてローカルの Gemini CLI に送信され、結果がSlackに返ってきます。

### 対象リポジトリの指定
複数のリポジトリを操作したい場合は、メッセージの先頭に `in <リポジトリ名>` を付けることで実行ディレクトリを切り替えられます。
*   例: `@bot in MyApp index.htmlの背景色を赤に変えて`
*   デフォルトの検索ベースディレクトリは `~/Desktop/develop` です（`.env`の `TARGET_BASE_DIR` で変更可能）。

## セットアップ

### 1. Slack Appの作成
1. [Slack API](https://api.slack.com/apps) にアクセスして「Create New App」を選択 (From scratch)
2. 「Socket Mode」を有効化し、App-Level Token (`xapp-...`) を発行
3. 「Event Subscriptions」で `app_mention` と `message.im` (必要に応じて) を追加
4. 「OAuth & Permissions」でBot Token (`xoxb-...`) を発行 (Scopes: `app_mentions:read`, `chat:write` など)

### 2. 環境変数の設定
`.env` ファイルを作成し、トークンを設定します。
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
TARGET_BASE_DIR=~/Desktop/develop  # 任意（対象リポジトリのベースディレクトリ）
```

### 3. 起動
```bash
pip install uv
uv sync
uv run python app.py
```
