# TokenBroker

TokenBroker is a tool that listens to callbacks from Microsoft OAuth applications, generates an access_token, saves it to disk, notifies the operator, and passes the token to other tools.

# How does it work?

TokenBroker acts as a callback endpoint for your Microsoft OAuth application.

It listens for an incoming authorization code after successful app authentication and user consent for your malicious app.

Then, TokenBroker submits the authorization code along with the `client_secret` and `client_id` to obtain a valid `access_token` with the scoped permissions for your app.

After acquiring the `access_token`, TokenBroker saves it to disk and passes it to a configured command, allowing the token to be reused by other tools such as AzureHound.

Note that this process only works if a user consents to your malicious app. In some tenants, a privileged user may be required to consent if the app has dangerous permissions.

Also, TokenBroker will use the `client_id` and the `callback_url` to generate a ready to use Oauth consent phishing link.

# Requirements

You can install all required packages by running `pip3 install -r requirements.txt`

# Usage

First of all, you need to modify `config.py` which contains the following:

```
#!/usr/bin/python3

TOKEN_URL = "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
CLIENT_ID = ""
CLIENT_SECRET = ""
CALLBACK_URL = ""
CALLBACK_PATH = ""
SLACK_WEB_HOOK = ""
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
SCOPES = "https://graph.microsoft.com/.default openid offline_access"


# Replace TOKENTOKEN with the token position in your command
POST_TOKEN_COMMAND = "azurehound list -j 'TOKENTOKEN' -o /tmp/output.json --graph https://graph.microsoft.com"
```


To be able to retreive an access token from Microsoft after a successful callback is made to your callback endpoint, you need to provide `CLIENT_ID`, `CLIENT_SECRET`, `CALLBACK_URL` and `CALLBACK_PATH` as part of your `config.py`.

Please check [this Guide](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app) from Microsoft for more details.

To receive a notifcation to a Slack channel when a token is captured, you can modify `SLACK_WEB_HOOK` and add your Slack webhook URL, otherwise you can leave it blank.

And if you need to use the captured token by other tools, you can set `POST_TOKEN_COMMAND` to the command you want to execute once the token is retreived and place the access_token poistion as `TOKENTOKEN` string in your command.

After editing `config.py` you are now ready TokenBroker.

To view TokenBroker options, you can simply pass `-h` to `TokenProker.py` as the following:

```
 /opt/red/TokenBroker  main !1 ?4  python3 TokenBroker.py -h              ✔ 

    
      _____ _____ _   __ _____ _   _ ______           _             
 |_   _|  _  | | / /|  ___| \ | || ___ \         | |            
   | | | | | | |/ / | |__ |  \| || |_/ /_ __ ___ | | _____ _ __ 
   | | | | | |    \ |  __|| . ` || ___ \ '__/ _ \| |/ / _ \ '__|
   | | \ \_/ / |\  \| |___| |\  || |_/ / | | (_) |   <  __/ |   
   \_/  \___/\_| \_/\____/\_| \_/\____/|_|  \___/|_|\_\___|_|   
                                                             
    
usage: TokenBroker.py [-h] --host HOST --port PORT [--private_key PRIVATE_KEY]
                      [--certificate CERTIFICATE]

AuthBroker args parser

options:
  -h, --help            show this help message and exit
  --host HOST           The webserver host to listen to
  --port PORT           The webserver port to listen to
  --private_key PRIVATE_KEY
                        SSL Certificate private key path
  --certificate CERTIFICATE
                        SSL Certificate path

 /opt/redteaming/TokenBroker  main !1 ?5                                                                                                                  ✔ 
```

# Resources

* [Protect against consent phishing](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/protect-against-consent-phishing)

* [Compromised and malicious applications investigation](https://learn.microsoft.com/en-us/security/operations/incident-response-playbook-compromised-malicious-app)