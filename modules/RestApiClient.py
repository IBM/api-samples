from urllib.error import HTTPError
from urllib.request import Request
from urllib.request import urlopen

import MakeConfig
import ReadConfig


# This is a simple HTTP client that can be used to access the REST API
class RestApiClient:

    # Constructor for the RestApiClient Class
    def __init__(self, settings=None, config_section='DEFAULT'):

        # Gets configuration information from config.ini. See ReadConfig
        # for more details.
        if not settings:
            settings = ReadConfig.main(config_section=config_section)
        if not settings:
            MakeConfig.main()
            settings = ReadConfig.main(config_section=config_section)

        # Set up the default HTTP request headers
        self.headers = {b'Accept': settings['accept']}
        if settings['version']:
            self.headers['Version'] = settings['version']

        # Set up the security credentials. We can use either an encoded
        # username and password or a security token
        if 'auth_token' in settings:
            self.auth = {'SEC': settings['auth_token']}
        else:
            self.auth = {'Authorization': settings['authorization']}

        self.headers.update(self.auth)

        # Set up the server's ip address and the base URI that will be used for
        # all requests
        self.server_ip = settings['server_ip']
        self.base_uri = '/api/'


    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None):

        path = self.parse_path(endpoint, params)

        # If custom headers are not specified we can use the default headers
        if not headers:
            headers = self.headers

        # Send the request and receive the response
        request = Request(
            'https://' + self.server_ip + self.base_uri + path, headers=headers)
        request.get_method = lambda: method
        try:
            # returns response object for opening url.
            return urlopen(request, data)
        except HTTPError as e:
            # an object which contains information similar to a request object
            return e

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
        return self.headers

    def get_server_ip(self):
        return self.server_ip

    def get_base_uri(self):
        return self.base_uri
