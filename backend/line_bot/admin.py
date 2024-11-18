from django.contrib import admin, messages
from .models import AutoChat, Notification, Tag, ChatRecord, GPTConfig
from django.urls import path
from django.http import HttpResponseRedirect
from .utils import save_chatbot_script_to_json
from decouple import config
from django.utils import timezone
from .openai_utils import prepare_gpt_dataset, fine_tuning_gpt


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
    MulticastRequest,  
    TextMessage,
   

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




class AutoChatAdmin(admin.ModelAdmin):
    search_fields = ['question', 'answer']
    list_display = ('question', 'answer')

    change_list_template = "line_bot/autochat/change_list.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super(AutoChatAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fine_tuned_action/', self.admin_site.admin_view(self.fine_tuned_action_view),
                 name='fine_tuned_action')
        ]
        return custom_urls + urls

    def fine_tuned_action_view(self, request):
        success=False

        save_chatbot_script_to_json() 
        prepare_gpt_dataset()
        status = fine_tuning_gpt()
        success = status

        message = ""
        if success:
            self.message_user(request, "เทรนข้อมูลสำเร็จ")
            message = "เทรนข้อมูลสำเร็จ"

        elif not success:
            self.message_user(request, "เทรนข้อมูลล้มเหลว", level=messages.ERROR)
            message = "เทรนข้อมูลล้มเหลว"

        user_notiications = Notification.objects.all() 
        if user_notiications:
            multicast_message = TextMessage(text=message) 
            un_uids = [un.line_uid for un in user_notiications]
        
            line_bot_api.multicast(MulticastRequest(
                        to=un_uids, messages=[multicast_message]))
     
        return HttpResponseRedirect("../")

class ChatRecordAdmin(admin.ModelAdmin):
    search_fields = ['question', 'answer']
    list_display = ('question', 'answer')
    
admin.site.register(AutoChat, AutoChatAdmin)
admin.site.register(Notification)
admin.site.register(Tag)
admin.site.register(ChatRecord, ChatRecordAdmin)
admin.site.register(GPTConfig)

