from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("hvdKUx0crJpGbVOTXroEKWzRUt2TMMjdjcDM3io6KjVGkTkUENkV7yEtj/Q54B3mLCRneZ7kyo5lQmqbr2F69miwofzlPJbwXYUipoaJCEQd4eYsfmmsKZV5PNsFtXm9e/PtwxXPHVf3fUbIiycucwdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.environ.get("2d53f3c45d710c572ed8c1493fbc52b7")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("LINE Channel Access Token / Secret が設定されていません。")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ここでスクレイピングやデータベース検索を入れることが可能
    # 今は受信したメッセージをそのまま返すサンプル
    text = event.message.text
    reply_text = f"あなたのメッセージ: {text}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
