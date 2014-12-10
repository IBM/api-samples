#!/usr/bin/env python3
# This sample demonstrates how to encode credentials, how to format and attach
# headers to an HTTP request, and how to send a simple request to a REST API
# endpoint. This script uses many python modules directly in order to
# demonstrate the low level functionality of the API. Future scripts will wrap
# this functionality into shared modules for re-use.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.

import base64
import configparser
import json
import sys
import os
import urllib.request

sys.path.append(os.path.realpath('../modules'))
import MakeConfig


def main():
    
    # For the purpose of this sample, credentials and settings are read
    # from plain text config files. It is recommended that you do not leave
    # secure credentials saved in these files.
    create_config_file()
    config = configparser.ConfigParser()
    config.read('../config.ini')

    username = config['DEFAULT']['username']
    password = config['DEFAULT']['password']
    server_ip = config['DEFAULT']['server_ip']

    # Credentials may be passed as the base 64 encoding of the string
    # username:password.
    userpass = username + ":" + password
    encoded_credentials = b"Basic " + base64.b64encode(userpass.encode('ascii'))

    # Note that base 64 encoding is not a secure form of encoding. The security
    # of the contents of requests relies on ssl encryption in the HTTPS
    # protocol. You should ensure that connections made to the REST API are
    # properly secured to ensure that sensitive information can not be
    # intercepted.
    print(encoded_credentials)

    # You must pass your credentials in the https request headers.
    # You may also specify the version of the API you want to use and the format
    # of the response you will receive. For the purpose of these samples,
    # version 2.0 of the API will be used and responses will be in JSON.
    # Note that if you pass a version number that does not exist, the API
    # will select the highest matching version lower than the one you requested
    # and use that version instead.
    headers = {'Version': '2.0', 'Accept': 'application/json', 'Authorization': encoded_credentials}
    print(headers)
    # You can also use a security token for authentication.
    # The format for passing a security token is "'SEC': token" instead of
    # "'Authorization': 'Basic encoded_credentials'".

    # REST API requests are made by sending an HTTPS request to specific URLs.
    url = 'https://' + server_ip + '/api/help/capabilities'
    print(url)
    # There are several base URL aliases that can be used to access the api.
    # As of this release '/api' is the preferred alias.

    # Here we are creating a GET request that will return a list of all
    # endpoints available to you on the system. This endpoint provides
    # details about what each endpoint does, the parameters they take and the
    # errors that can occur when you use them.
    request = urllib.request.Request(url, headers=headers)

    # Here we are sending the request and receiving a response.
    response = urllib.request.urlopen(request)

    # Since we requested that the data be returned to us in JSON format, we can
    # parse it using standard JSON modules. Note that because we have requested
    # information about all endpoints on the system, the response may be quite
    # long.
    parsed_response = json.loads(response.read().decode('utf-8'))
    print(json.dumps(parsed_response, indent=4))
    
    # Each response contains an HTTP response code.
    # Response codes in the 200 range indicate that your request succeeded.
    # Response codes in the 400 range indicate that your request failed due to
    # incorrect input.
    # Response codes in the 500 range indicate that there was an error on the
    # server side.
    print(response.code)
    
    # Here we can see the headers of the response, including the session cookie.
    print(response.headers)


# This function invokes the interactive config file creator if no config file
# exists.
def create_config_file():
    filename = os.path.join(os.getcwd(), "../config.ini")
    if os.path.isfile(filename):
        return
    else:
        MakeConfig.main()
        return

if __name__ == "__main__":
    main()
