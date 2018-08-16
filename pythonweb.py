from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

import requests # pip install requests

import urllib3


app = Flask(__name__)

#Token
line_bot_api = LineBotApi('tgBlH/o6bTRXjdKuLC3QQ/42RefujzBGP/JPwagMHdpoh0+qQBcIoIJH+PvmRZmepqHG9UdSDvkWNLEWHcC5E5SfptTgPKsgcMgQzFj9nDOE5tT/ULtObrhqhc9WMe/HqeWN7GqzwfBfOhftArE0kgdB04t89/1O/w1cDnyilFU=')
#Channel secret
handler = WebhookHandler('85e93a3b16a648dafd2da84f1a9f9f3e')

APPID="BotChatLine"
KEY = "me37I8KsiCqpTWS"
SECRET = "ozPtNGTK6GPA1STe1PjIvvrwS"
Topic = "/LED_Control_TESR"

url = 'https://api.netpie.io/topic/' + str(APPID) + str(Topic)
#curl -X PUT "https://api.netpie.io/topic/LineBotRpi/LED_Control" -d "ON" -u Jk0ej35pLC7TVr1:edWzwTUkzizhlyRamWWq6nF9I 

urlRESTAPI = 'https://api.netpie.io/topic/' + str(APPID) + str(Topic) + '?auth=' + str(KEY) + ':' + str(SECRET)
#https://api.netpie.io/topic/LineBotRpi/LED_Control?auth=Jk0ej35pLC7TVr1:edWzwTUkzizhlyRamWWq6nF9I


@app.route("/callback_TESR", methods=['POST'])
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	#global url , KEY , SECRET
    if "on" in str(event.message.text):
    	line_bot_api.reply_message(event.reply_token,TextSendMessage(text='ON LED'))

    	#REST API NETPIE ON LED
    	r = requests.put(url, data = {'':'ON'} , auth=(str(KEY),str(SECRET)))
		
    elif "off" in str(event.message.text): #elif
    	line_bot_api.reply_message(event.reply_token,TextSendMessage(text='OFF LED'))

    	#REST API NETPIE OFF LED
    	r = requests.put(url, data = {'':'OFF'} , auth=(str(KEY),str(SECRET)))
	
    elif "menu" in str(event.message.text):
    	#line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Menu'))

	#image_message  = ImageSendMessage(original_content_url='https://www.picz.in.th/images/2018/08/16/BHk2VV.jpg',preview_image_url='https://www.picz.in.th/images/2018/08/16/BHk2VV.jpg')
	#line_bot_api.push_message('ItfoFj89IMTUAR2ERKN1yPxAPZk4UvEC4fperPkGrCg/L6GwTXKR/sOC1KEYyMJppqHG9UdSDvkWNLEWHcC5E5SfptTgPKsgcMgQzFj9nDNTaJlDhv/Xw+0ahLBCWC8nO8sMe6GSGd+dP6fmoFMPNwdB04t89/1O/w1cDnyilFU=', image_message)
	#line_bot_api.reply_message(event.reply_token,TextSendMessage(text='https://www.picz.in.th/images/2018/08/16/BHYO9V.jpg'))
	#line_bot_api.reply_message(event.reply_token, image_message )
	location_message = LocationSendMessage(
    		title='my location',
    		address='Tokyo',
    		latitude=35.65910807942215,
    		longitude=139.70372892916203
	)
	
	#sticker_message = StickerSendMessage(package_id='1',sticker_id='1')
	line_bot_api.reply_message(event.reply_token, location_message )

    	#--REST API NETPIE OFF LED--
    	r = requests.put(url, data = {'':'Menu'} , auth=(str(KEY),str(SECRET)))

    elif "temp?" in str(event.message.text):
    	#REST API NETPIE read sensor value
    	r = requests.put(url, data = {'':'temp?'} , auth=(str(KEY),str(SECRET)))
    	
    	http = urllib3.PoolManager()
    	response = http.request('GET',urlRESTAPI) # read data from publish retain

    	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=((str(response.data)).split('"')[7]) + " °C"))
        
        #r = requests.get(urlRESTAPI)
        #https://api.netpie.io/topic/LineBotRpi/LED_Control?auth=Jk0ej35pLC7TVr1:edWzwTUkzizhlyRamWWq6nF9I
        
    else:
    	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
