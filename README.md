 ## 功能：
 #### 以個人帳號上傳圖片至官方帳號，將自動將圖片上傳至imgur圖床，並傳送至有加入該官方帳號之群組。

 ## 安裝：
 #### 1.LINE取得Channel_Secret及Channel_Access_Token
 #### 2.Imgur取得Imgur_Access_Token(需使用POSTMAN：參考https://vocus.cc/article/66628ec1fd89780001f89f7f)
 #### 3.環境變數設定為:
  - Channel_Access_Token = '取得之Channel_Access_Token'
  - Channel_Secret = '取得之Channel_Secret'
  - Imgur_Access_Token = '取得之Imgur_Access_Token'
 #### 4. 開啟Use webhook功能，並部署於雲端，將Webhook settings設為部署服務之網址，
 
 ## 使用：
 
 - 官方帳號加入至群組後，自動加入/註銷該群組為推送圖片之範圍
 - 使用註冊為管理員之個人帳號，直接傳送圖片至官方帳號，則自動上傳至imgur及推送圖片至各群組
 - 個人帳號傳送官方帳號相關指令如下
   - @註冊@ : 註冊為管理者
   - @註銷@ : 註銷管理者
   - @查看群組@ : 查看目前官方帳號加入之群組名稱
   - @查看管理者@ : 查看目前註冊為管理者之個人帳號名稱
 
 
