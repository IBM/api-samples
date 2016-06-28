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
# at the /api/help/versions endpoint.

import base64
import configparser
import json
import ssl
import sys
import os
import urllib.request
import getpass


def main():

    # Prompt for server host and credentials.
    host = input("Please input the IP address or the hostname of the server " +
                 "you want to connect to: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    certificate_file = input(
        "Enter path to TLS PEM certificate (optional): ").strip()

    # Credentials may be passed as the base 64 encoding of the string
    # username:password.
    userpass = username + ":" + password
    encoded_credentials = b"Basic " + base64.b64encode(
        userpass.encode('ascii'))

    # Note that base 64 encoding is not a secure form of encoding. The security
    # of the contents of requests relies on ssl encryption in the HTTPS
    # protocol. You should ensure that connections made to the REST API are
    # properly secured to ensure that sensitive information can not be
    # intercepted.
    print(encoded_credentials)

    # You must pass your credentials in the https request headers.
    # You may also specify the version of the API you want to use and the
    # format of the response you will receive. For the purpose of these
    # samples, version 6.0 of the API will be used and responses will be in
    # JSON. Note that if you pass a version number that does not exist, the API
    # will select the highest matching version lower than the one you requested
    # and use that version instead.
    headers = {'Version': '6.0', 'Accept': 'application/json',
               'Authorization': encoded_credentials}
    print(headers)
    # You can also use a security token for authentication.
    # The format for passing a security token is "'SEC': token" instead of
    # "'Authorization': 'Basic encoded_credentials'".

    # Python version 3.4.2 and before by default do not perform certificate
    # validation. Here we will set up an SSLContext that performs certificate
    # validation. ssl.PROTOCOL_SSLv23 is misleading. PROTOCOL_SSLv23 will use
    # the highest version of SSL or TLS that both the client and server
    # supports.
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

    # SSL version 2 and SSL version 3 are insecure. The insecure versions are
    # disabled.
    try:
        context.options = ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
    except ValueError as e:
        # Disabling SSLv2 and SSLv3 is not supported on versions of OpenSSL
        # prior to 0.9.8m.
        print('WARNING: Unable to disable SSLv2 and SSLv3, caused by '
              'exception: "' + str(e) + '"')
        while True:
            response = input(
                "Would you like to continue anyway (yes/no)? ").strip().lower()
            if response == "no":
                sys.exit(1)
            elif response == "yes":
                break
            else:
                print(response + " is not a valid response.")

    # Require certificate verification.
    context.verify_mode = ssl.CERT_REQUIRED
    # By default we are going to enable hostname verification.
    # context.check_hostname is only available on Python version 3.4 and above.
    # On Python version 3.3 check_hostname parameter on the HTTPSHandler is
    # used.
    if sys.version_info >= (3, 4):
        context.check_hostname = True
    check_hostname = True

    if certificate_file != "":
        # An optional certificate file was provided by the user.

        # The default QRadar certificate does not have a valid hostname so we
        # must disable hostname checking.
        if sys.version_info >= (3, 4):
            context.check_hostname = False
        check_hostname = False

        # Load the certificate file that was specified by the user.
        context.load_verify_locations(cafile=certificate_file)
    else:
        # The optional certificate file was not provided. Load the default
        # certificates.
        if sys.version_info >= (3, 4):
            # Python 3.4 and above has the improved load_default_certs()
            # function. This should work on most systems.
            context.load_default_certs(ssl.Purpose.CLIENT_AUTH)
        else:
            # Versions of Python before 3.4 do not have the
            # load_default_certs method.  set_default_verifypaths will
            # work on some, but not all systems.  It fails silently.  If
            # this call fails the certificate will fail to validate.
            # This will never work on Windows. Windows users should upgrade
            # to Python 3.4 or later.
            context.set_default_verify_paths()

    # Create a new HTTPSHandler and install it using the new HTTPSContext.
    urllib.request.install_opener(urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=context,
                                    check_hostname=check_hostname)))

    # REST API requests are made by sending an HTTPS request to specific URLs.
    url = 'https://' + host + '/api/help/versions'
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

    # Here we can see the headers of the response.
    print(response.headers)


if __name__ == "__main__":
    main()
