import os
import subprocess
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def run_command(cmd_str, cwd=None):
    try:
        # NOTE: In production, consider security implications. Use shlex/safe command parsing if accepting user input.
        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=30, cwd=cwd)
        output = result.stdout if result.stdout else result.stderr
        return output if output else "✅ 実行完了（出力なし）"
    except Exception as e:
        return f"❌ エラーが発生しました: {str(e)}\n\n(cwd: {cwd})"

@app.event("app_mention")
def handle_app_mentions(event, say):
    text = event.get("text", "")
    
    # Extract the prompt. If the user just mentions the bot, the whole text (minus the mention) is the prompt.
    # The text usually looks like "<@U12345678> hello gemini", so we strip out the mention.
    import re
    # Remove user mentions like <@U0123ABCD>
    prompt = re.sub(r'<@U[A-Z0-9]+>', '', text).strip()
    
    if not prompt:
        say("プロンプトを入力してください。\n例: `@bot in MyApp 背景色を赤に変えて`")
        return
        
    # Check for "in <repo>" format
    target_dir = None
    target_repo = None
    
    # Match "in <repo> <prompt>"
    match = re.match(r'^in\s+([^\s]+)\s+(.+)$', prompt, re.IGNORECASE)
    if match:
        target_repo = match.group(1)
        prompt = match.group(2).strip()
        
        # Determine base directory
        base_dir = os.environ.get("TARGET_BASE_DIR", os.path.expanduser("~/Desktop/develop"))
        target_dir = os.path.join(base_dir, target_repo)
        
        # Validate directory exists
        if not os.path.isdir(target_dir):
            say(f"❌ リポジトリディレクトリが見つかりません: `{target_dir}`")
            return
            
        say(f"📂 リポジトリ `{target_repo}` でGemini CLIに問い合わせ中...\\nプロンプト: `{prompt}`")
    else:
        say(f"🤖 (デフォルトディレクトリ) Gemini CLIに問い合わせ中...\\nプロンプト: `{prompt}`")
    
    # Run gemini cli with the prompt securely
    import shlex
    safe_prompt = shlex.quote(prompt)
    out = run_command(f'gemini {safe_prompt}', cwd=target_dir)
    say(f"結果:\\n```\\n{out}\\n```")

if __name__ == "__main__":
    app_token = os.environ.get("SLACK_APP_TOKEN")
    if not app_token:
        print("エラー: SLACK_APP_TOKEN が設定されていません。")
        exit(1)
        
    print("⚡️ Slack Mac Controller 起動中...")
    handler = SocketModeHandler(app, app_token)
    handler.start()
