#web_app
#flask,django都是架設伺服器用，其中flask規模小(app用),django規模大(網頁用)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('cT4rd/AKMW7Nv0vcqIuPNTYW/3qXGdGG+PE/a6YQ0eWfGBQjolyTklsC9/BRfNh/UAR+LQEawf5z9n1207CMjyO8e3yeVWzMuFmGOYwfRwFfNb2BUx6fVys3x5vemtt+3wUB2pNMb3NJa1Y+cgTuHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1d3b3fdd89459222c11c1ef06ce72462')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()