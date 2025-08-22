from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

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
from flask import Flask, request, jsonify
from urllib.parse import quote_plus

app = Flask(__name__)

@app.route("/search_url", methods=["GET"])
def search_url():
    query = request.args.get("query")  # 商品名でもJANコードでもOK
    if not query:
        return jsonify({"error": "query parameter is required"}), 400

    # URLエンコードして検索用URLを作成
    encoded_query = quote_plus(query)
    search_url = f"https://www.x-jpn.co.jp/?item_work=&item_series=&item_maker=&s={encoded_query}"

    return jsonify({"search_url": search_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    


    
    # ここでスクレイピングやデータベース検索を入れることが可能
    # 今は受信したメッセージをそのまま返すサンプル
    # text = event.message.text
    # reply_text = f"あなたのメッセージ: {text}"
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
