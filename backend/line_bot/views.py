from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import re

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, JsonResponse, HttpResponseRedirect
from decouple import config



from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
from .utils import generate_simple_answer, record_chat
from .openai_utils import generate_gpt_answer


# line
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError,

)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    VideoMessage,
    ImagemapMessage,
    ImagemapArea,
    URIImagemapAction,
    ImagemapBaseSize,
    MessageAction,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    PushMessageRequest,
    FlexMessage,
    FlexContainer,
    ApiException,
    ErrorResponse,
    MulticastRequest,

)
from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
    TextMessageContent,

)






ACCESS_TOKEN = config('LINE_ACCESS_TOKEN')
SECRET_TOKEN = config('LINE_SECRET_TOKEN')
configuration = Configuration(access_token=ACCESS_TOKEN)
handler = WebhookHandler(SECRET_TOKEN)
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)


@csrf_exempt
def index(request):
    if request.method == 'POST':
        signature = request.headers.get('X-Line-Signature')
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest("Invalid signature. Please check your channel access token/channel secret.")

        return HttpResponse("OK")


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):

    message = (event.message.text).lower()
    user_id = event.source.user_id
   

  
    username = line_bot_api.get_profile(user_id).display_name
    

    if "#myid" in message:
        mess = TextMessage(text=user_id)
        line_bot_api.reply_message(ReplyMessageRequest(
                replyToken=event.reply_token, messages=[mess]))
    else:
        response_tag, response_answer = generate_simple_answer(message)
        if response_tag != "unknown":

            if "--img--" in response_answer:
                split_answer = response_answer.split("--img--")
                answer = split_answer[0]
                img_url = split_answer[1]
                mess = TextMessage(text=answer)
                mess_img = ImageMessage(originalContentUrl=img_url, previewImageUrl=img_url)
                line_bot_api.reply_message(ReplyMessageRequest(replyToken=event.reply_token, messages=[mess, mess_img]))                
            else:
                mess = TextMessage(text=response_answer)
                line_bot_api.reply_message(ReplyMessageRequest(
                replyToken=event.reply_token, messages=[mess]))

            record_chat(question=message, answer=response_answer, user=username)
        else:
            answer = generate_gpt_answer(message)
            mess = TextMessage(text=answer) 
            line_bot_api.reply_message(ReplyMessageRequest(
                replyToken=event.reply_token, messages=[mess]))


            record_chat(question=message, answer=answer, user=username, source="GPT-AI")


   

