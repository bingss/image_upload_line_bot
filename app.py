from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    JoinEvent,
    LeaveEvent,
    TextMessageContent,
    ImageMessageContent
)
import os
import requests
import idFileManager

app = Flask(__name__)
configuration = Configuration(access_token=os.getenv('Channel_Access_Token'))
line_handler = WebhookHandler(os.getenv('Channel_Secret'))

# Imgur API
IMGUR_ACCESS_TOKEN = os.getenv('Imgur_Access_Token')

# 儲存id txt path
managerid_filepath = "./tmp/managerid_file.txt"
group_id_filepath = "./tmp/group_id_file.txt"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("channel access token/channel secret錯誤，請再次檢查.")
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=(ImageMessageContent))
def handle_message(event):
    with ApiClient(configuration) as api_client:
        group_id_set = idFileManager.read_all_ids(group_id_filepath)
        managerid_set = idFileManager.read_all_ids(managerid_filepath)
        # 限制只有特定使用者且非群組內訊息才能上傳圖片
        if event.source.type != "user" or managerid_set.__contains__(event.source.user_id) == False:
            return
        
        line_bot_api = MessagingApi(api_client)
        if isinstance(event.message, ImageMessageContent):
            # 獲取圖片內容
            line_bot_blob_api = MessagingApiBlob(api_client)
            message_content = line_bot_blob_api.get_message_content(event.message.id)
            try:
                if(len(group_id_set) == 0):
                    raise Exception('尚無待傳送群組ID')
                # 將圖片數據上傳到 Imgur
                url = "https://api.imgur.com/3/image"
                payload = {'type': 'file',
                'title': event.message.id,
                'description': 'upload in Imgur'}
                files = {"image": message_content}
                headers = {'Authorization': f'Bearer {IMGUR_ACCESS_TOKEN}'}
                response = requests.request('POST', url, headers=headers, data=payload, files=files)
                response_data = response.json()
                if response_data['success']:
                    imgur_url = response_data['data']['link']
                    # 建立圖片訊息
                    image_message = ImageMessage(
                        original_content_url=imgur_url,
                        preview_image_url=imgur_url
                    )
                else:
                    raise Exception('Imgur 上傳失敗')
                
                # 推送圖片訊息至特定群組
                group_name_array = []
                for group_id in group_id_set:
                    line_bot_api.push_message_with_http_info(
                        PushMessageRequest(
                            to=group_id,
                            messages=[image_message]
                        )
                    )
                    group_name_array.append(line_bot_api.get_group_summary(group_id).group_name)
                # 回傳推送成功訊息
                reply_text = f'圖片:{imgur_url}\n已成功發送至群組:{",".join(group_name_array)}'
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_text)]
                    )
                )
            except Exception as e:
                reply_text = f'圖片傳送失敗: {e}'
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_text)]
                    )
                )

@line_handler.add(MessageEvent, message=(TextMessageContent))
def handle_message(event):
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        reply_text = None
        group_id_set = idFileManager.read_all_ids(group_id_filepath)
        managerid_set = idFileManager.read_all_ids(managerid_filepath)
        
        if event.source.type == 'user':
            user_id = event.source.user_id
            if user_id in managerid_set:
                if event.message.text == '@註銷@':
                    idFileManager.delete_id(event.source.user_id, managerid_filepath)
                    reply_text = '已註銷上傳管理者'
                elif event.message.text == '@查看管理者@':
                    authorized_user_name_array = []
                    for user_id in managerid_set:
                        authorized_user_name_array.append(line_bot_api.get_profile(user_id).display_name)
                    reply_text = f'上傳管理者:{",".join(authorized_user_name_array)}'
                elif event.message.text == '@查看群組@':
                    group_name_array = []
                    for group_id in group_id_set:
                        group_name_array.append(line_bot_api.get_group_summary(group_id).group_name)
                    reply_text = f'群組:{",".join(group_name_array)}'
            if event.message.text == '@註冊@':
                idFileManager.save_id(user_id, managerid_filepath)
                reply_text = '註冊為上傳管理者'
                
        if reply_text != None:
            # 傳送文字訊息回覆
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )

# 監聽 JoinEvent
@line_handler.add(JoinEvent)
def handle_join(event):
    try:
        # 獲取群組 ID
        if event.source.type == "group":
            group_id = event.source.group_id
            idFileManager.save_id(group_id, group_id_filepath)
            print(f"Bot 已加入群組，群組 ID: {group_id}")

    except Exception as e:
        print(f"Error: {e}")

@line_handler.add(LeaveEvent)
def handle_leave(event):
    try:
        # group_id_set = idFileManager.read_all_ids(group_id_filepath)
        # # 獲取群組 ID
        # if event.source.type == "group":
        #     group_id = event.source.group_id
        #     if group_id in group_id_set:
        #         group_id_set.remove(group_id)

        group_id = event.source.group_id
        idFileManager.delete_id(group_id, group_id_filepath)
        print(f"Bot 已離開群組，群組 ID: {group_id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app.run()