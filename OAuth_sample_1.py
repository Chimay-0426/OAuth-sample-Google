#python関連ライブラリ。
 from pydrive.auth import GoogleAuth
 #from pydrive.drive import GoogleDrive
 import gspread
 #GoogleOauth認証関連ライブラリ。
 from google.auth.transport.requests import Request
 from google.oauth2.credentials import Credentials
 from googleapiclient.discovery import build
 from googleapiclient.errors import HttpError
 from apiclient.http import MediaFileUpload
 from googleapiclient.discovery import build
 from google_auth_oauthlib.flow import InstalledAppFlow


 #ダウンロードした認証情報が保管してあるローカルのフォルダへのパス。GoogleAPIの認証画面で取得したjsonファイルを格##納するディレクトリーに格納。
 CREDENTIAL_DIR = "~"

 #認証情報ファイルまでのパス
 CLIENT_SECRET_FILE = os.path.join(CREDENTIAL_DIR, 'client_secret.json')

 #一旦API認証が成功した後の認証情報を記録するファイルのパス
 CREDENTIAL_PATH = os.path.join(CREDENTIAL_DIR, 'credential.json')

 #GoogleAPIで用いたAppNameを使用。
 APPLICATION_NAME = "~"

 #以下で操作する範囲のAPIエンドポイントを定義。
 SCOPES = "https://www.googleapis.com/auth/spreadsheets"

 #OAuth認証。
 def get_credential():
 #credentialファイルが存在すれば、それで認証する。
     creds = None
     if os.path.exists(CREDENTIAL_PATH):
         #credsに返り値であるcredentialsが格納される。
         creds = Credentials.from_authorized_user_file(CREDENTIAL_PATH, SCOPES)
 # 未認証だった場合は許可を求める(ブラウザ認証)。
 #credsに代入されていない場合、または、tokenが代入されていてもexpireしている場合次のif文の処理に移る。
     if not creds or not creds.valid:
         #credsに代入されていて、expireされていて、OAuthがtokenをrefreshする場合。
         if creds and creds.expired and creds.refresh_token:
             #アクセスtokenをrefreshする。括弧内のparameterはhttp request。
             creds.refresh(Request())
         else:
             #client_secrets_fileからFlowインスタンスを生成。
             flow = InstalledAppFlow.from_client_secrets_file(
                 CLIENT_SECRET_FILE, SCOPES)
             #OAuth2.0のcreedentialに返す。credsに代入、
             creds = flow.run_local_server(port=0)
 # 次回のためにcredential.jsonというファイルを書き込み権限で起案し、to_jsonでcredentialをJSON形式に生成。
         with open('credential.json', 'w') as token:
             token.write(creds.to_json())
     return creds
