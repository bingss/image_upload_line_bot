 ## 功能：
 #### 以個人帳號上傳圖片至官方帳號，自動將圖片上傳至imgur圖床，並推送至有加入該官方帳號之群組。管理者之個人帳號及有加入官帳之群組則自動以google sheet儲存。
 #### 注意:
  - 每月免費推送至群組或帳號訊息為200則
  - 傳送圖片後稍等4-5秒，傳送成功或失敗皆會有回復訊息。

 ## 安裝：
 #### 1.LINE取得Channel_Secret及Channel_Access_Token。
 #### 2.Imgur取得Imgur_Access_Token(需使用POSTMAN：參考https://vocus.cc/article/66628ec1fd89780001f89f7f)。
 #### 2.GoogleSheet取得憑證(參考[https://vocus.cc/article/66628ec1fd89780001f89f7f](https://www.youtube.com/watch?v=tPfllMdhCUE))。
 #### 3.環境變數設定為:
  - Channel_Access_Token = '取得之Channel_Access_Token'
  - Channel_Secret = '取得之Channel_Secret'
  - Imgur_Access_Token = '取得之Imgur_Access_Token'
  - Google_Sheet_Url='Google_Sheet連結' ==>開2個工作頁
  - Google_Credentials = 'Google憑證json(編輯為一行字串)'

 #### 4. 開啟Use webhook功能，並部署於雲端，將Webhook settings設為部署服務之網址'{服務網址}/callback'。
 
 ## 使用：
 - 官方帳號加入至群組後，自動加入/註銷該群組為推送圖片之範圍
 - 使用註冊為管理員之個人帳號，直接傳送圖片至官方帳號，則自動上傳至imgur及推送圖片至各群組
 - 個人帳號傳送官方帳號相關指令如下
   - @註冊@ : 註冊為管理者
   - @註銷@ : 註銷管理者
   - @查看群組@ : 查看目前官方帳號加入之群組名稱
   - @查看管理者@ : 查看目前註冊為管理者之個人帳號名稱
 
  ## 測試畫面：
<img src="https://github.com/user-attachments/assets/36107b3b-09f3-42f7-b772-84896c530deb" height="32%" width="32%" />
<img src="https://github.com/user-attachments/assets/c8825c48-e18d-477d-8e05-7a22cb3074cd" height="32%" width="32%" />
<img src="https://github.com/user-attachments/assets/04c22295-0a3c-473b-8d4e-06569916005d" height="32%" width="32%" />
