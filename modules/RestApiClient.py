from config import Config

from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import install_opener
from urllib.request import build_opener
from urllib.request import HTTPSHandler
from urllib.request import HTTPCookieProcessor
import http.cookiejar
import http.cookies

import ssl
import sys
import base64

# This is a simple HTTP client that can be used to access the REST API
class RestApiClient:

    # Constructor for the RestApiClient Class
    def __init__(self, config_section='DEFAULT', version=None, config=None):

        if config is None:
            self.config = Config(config_section=config_section)
        else:
            self.config = config

        self.headers = {'Accept': 'application/json'}
        if version is not None:
            self.headers['Version'] = version
        if self.config.has_config_value('auth_token'):
            self.headers['SEC'] = self.config.get_config_value('auth_token')
        elif self.config.has_config_value('username') and self.config.has_config_value('password'):
            username = self.config.get_config_value('username')
            password = self.config.get_config_value('password')
            self.headers['Authorization'] = b"Basic " + base64.b64encode((username + ':' + password).encode('ascii'))
        else:
            raise Exception('No valid credentials found in configuration.')

        self.server_ip = self.config.get_config_value('server_ip')
        self.base_uri = '/restapi/api/'

        self.cookies = http.cookiejar.CookieJar()

        # Create a secure SSLContext
        # PROTOCOL_SSLv23 is misleading.  PROTOCOL_SSLv23 will use the highest
        # version of SSL or TLS that both the client and server supports.
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.options = ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
        context.verify_mode = ssl.CERT_REQUIRED
        if sys.version_info >= (3, 4):
            context.check_hostname = True

        check_hostname = True
        certificate_file = self.config.get_config_value('certificate_file')
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

        install_opener(build_opener(HTTPCookieProcessor(self.cookies), HTTPSHandler(context=context, check_hostname=check_hostname)))

        # Send an initial GET request so that we can obtain the required
        # session cookie.
        self.call_api('help/capabilities?categories=["help"]', 'GET')

    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None):

        path = self.parse_path(endpoint, params)

        # If the caller specified customer headers merge them with the default
        # headers.
        actual_headers = self.headers.copy();
        if headers is not None:
            for header_key in headers:
                actual_headers[header_key] = headers[header_key]

        # Send the request and receive the response
        request = Request(
            'https://' + self.server_ip + self.base_uri + path, headers=actual_headers)
        request.get_method = lambda: method

        try:
            # returns response object for opening url.
            return urlopen(request, data)
        except HTTPError as e:
            # an object which contains information similar to a request object
            return e
        except URLError as e:
            if isinstance(e.reason, ssl.SSLError) and e.reason.reason == "CERTIFICATE_VERIFY_FAILED":
                print("Certificate verification failed.")
                sys.exit(3)
            else:
                raise e

    # This method constructs the query string
    def parse_path(self, endpoint, params):

        path = endpoint + '?'

        if isinstance(params, list):

            for kv in params:
                if kv[1]:
                    path += kv[0]+'='+kv[1]+'&'
            
        else:
            for k, v in params.items():
                if params[k]:
                    path += k+'='+v+'&'

        # removes last '&' or hanging '?' if no params.
        return path[:len(path)-1]


    # Simple getters that can be used to inspect the state of this client.
    def get_headers(self):
        return self.headers.copy()

    def get_server_ip(self):
        return self.server_ip

    def get_base_uri(self):
        return self.base_uri
