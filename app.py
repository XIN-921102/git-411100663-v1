# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('18sxPYYTraBvRW+g33n4KZYFO+IIpsUqJIEpv5GCcEer+sUDHc4B1yu7VNGgRIsp7RwpThd8MGnjzXsO6BtzS4JELG+0CyZi2fbpK3e8GGb+eEmNSo8hZdTeEHQDiLGkXRp14/KAvY8aO4AGgwlulAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('0c35f408217c3cb150bdf578831590a9')

line_bot_api.push_message('Ue2913ac9fb19e6301bd5067f3b2ca459', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/xMUKNtn.jpg',
            alt_text='組圖訊息',
            base_size=BaseSize(height=2000, width=2000),
            actions=[
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Cebu',
                    area=ImagemapArea(
                        x=0, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Taipei',
                    area=ImagemapArea(
                        x=1000, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Osaka',
                    area=ImagemapArea(
                        x=0, y=1000, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Shanghai',
                    area=ImagemapArea(
                        x=1000, y=1000, width=1000, height=1000
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
