#!/usr/bin/python3


TOKEN_URL = "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
CLIENT_ID = "94c15b0a-afde-4ddf-a29f-ae8ab493c521"
CLIENT_SECRET = "szb8Q~9kLy0Q0XhM37CLSWuQmcIgD~yElr3QBc8s"
CALLBACK_URL = "http://localhost:9000/callback"
CALLBACK_PATH = "/callback"
SLACK_WEB_HOOK = ""
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
SCOPES = "https://graph.microsoft.com/.default openid offline_access"


# Replace TOKENTOKEN with the token position in your command
POST_TOKEN_COMMAND = "azurehound list -j 'TOKENTOKEN' -o /tmp/output.json --graph https://graph.microsoft.com"

