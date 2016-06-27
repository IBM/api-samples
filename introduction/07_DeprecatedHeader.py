#!/usr/bin/env python3
# This sample demonstrates the Deprecated response header. The Deprecated
# response header is returned for each request to a deprecated API endpoint.

from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import build_opener
from urllib.request import HTTPSHandler
from urllib.request import install_opener
from urllib.request import Request
from urllib.request import urlopen

import base64
import os
import ssl
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
config_module = importlib.import_module('config')


def main():
    """
    The entry point for the sample.
    """

    config = config_module.Config()

    # Specify Version 4.0 in the request headers. Version 4.0 is a deprecated
    # version of the API.
    headers = {'Accept': 'application/json',
               'Version': '4.0'}
    if config.has_config_value('auth_token'):
        headers['SEC'] = config.get_config_value('auth_token')
    elif (config.has_config_value('username') and
            config.has_config_value('password')):
        headers['Authorization'] = b"Basic " + base64.b64encode(
            (config.get_config_value('username') + ':' +
             config.get_config_value('password')).encode('ascii'))
    else:
        raise Exception('No valid credentials found in configuration.')

    # Create a secure ssl conneciton.
    create_secure_ssl_context(config)

    url = ('https://' + config.get_config_value('server_ip') +
           '/api/reference_data/sets')

    # Call the API with a deprecated version.
    response = None
    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
    except HTTPError as e:
        response = e
    except URLError as e:
        if (isinstance(e.reason, ssl.SSLError) and
                e.reason.reason == "CERTIFICATE_VERIFY_FAILED"):
            print("Certificate verification failed.")
            sys.exit(1)
        else:
            raise e

    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("Failed to get reference sets.")
        print(response_body)
        sys.exit(1)

    # Headers can be found in the response info.
    response_info = response.info()

    # Since we called a deprecated version of the API we expect the Deprecated
    # header to be set.
    if 'Deprecated' in response_info:

        print("The response has a Deprecated header. This is the content of "
              "the Deprecated header:")
        print(response_info['Deprecated'])

    else:

        print("The response did not have a Deprecated header.")


def create_secure_ssl_context(config):
    """
    Create a and install a HTTPSHandler using a secure SSLContext.
    """

    # Create a secure SSLContext
    # PROTOCOL_SSLv23 is misleading.  PROTOCOL_SSLv23 will use the highest
    # version of SSL or TLS that both the client and server supports.
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

    # SSL version 2 and SSL version 3 are insecure. The insecure versions are
    # disabled.
    try:
        context.options = ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
    except ValueError as e:
        # Disabling SSLv2 and SSLv3 is not supported on versions of OpenSSL
        # prior to 0.9.8m.
        if not (config.has_config_value('ssl_2_3_ok') and
                config.get_config_value('ssl_2_3_ok') == 'true'):
            print('WARNING: Unable to disable SSLv2 and SSLv3. Caused by "'
                  'exception "' + str(e) + '"')
            while True:
                response = input(
                    "Would you like to continue anyway (yes/no)? "
                    ).strip().lower()
                if response == "no":
                    sys.exit(1)
                elif response == "yes":
                    config.set_config_value('ssl_2_3_ok', 'true')
                    break
                else:
                    print(response + " is not a valid response.")

    context.verify_mode = ssl.CERT_REQUIRED
    if sys.version_info >= (3, 4):
        context.check_hostname = True

    check_hostname = True
    certificate_file = config.get_config_value('certificate_file')
    if certificate_file is not None:
        # Load the certificate if the user has specified a certificate
        # file in config.ini.

        # The default QRadar certificate does not have a valid hostname,
        # so me must disable hostname checking.
        if sys.version_info >= (3, 4):
            context.check_hostname = False
        check_hostname = False

        # Instead of loading the default certificates load only the
        # certificates specified by the user.
        context.load_verify_locations(cafile=certificate_file)
    else:
        if sys.version_info >= (3, 4):
            # Python 3.4 and above has the improved load_default_certs()
            # function.
            context.load_default_certs(ssl.Purpose.CLIENT_AUTH)
        else:
            # Versions of Python before 3.4 do not have the
            # load_default_certs method.  set_default_verify_paths will
            # work on some, but not all systems.  It fails silently.  If
            # this call fails the certificate will fail to validate.
            context.set_default_verify_paths()

    install_opener(build_opener(
        HTTPSHandler(context=context, check_hostname=check_hostname)))

if __name__ == "__main__":
    main()
