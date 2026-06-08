from flask import Flask, request, abort, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import config
import commands
import listeners

app = Flask(__name__)
line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(config.CHANNEL_SECRET)

@app.route("/")
def home():
    return "Hello, World!"


@app.route("/favicon.ico")
@app.route("/favicon.png")
def favicon():
    return "OK"


@app.route("/mygo_images/<path:image_name>", methods=["GET"])
def mygo_image(image_name):
    return send_from_directory(str(config.MYGO_STATIC_DIR), image_name)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text: str = event.message.text
    reply_messages: list = []

    command_result = commands.dispatch(text)
    if command_result:
        reply_messages.extend(command_result)

    listener_result = listeners.check_all(text)
    if listener_result:
        reply_messages.extend(listener_result)

    if reply_messages:
        line_bot_api.reply_message(event.reply_token, reply_messages)


if __name__ == "__main__":
    app.run(debug=True)
