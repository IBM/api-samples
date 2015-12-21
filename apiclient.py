#!/usr/bin/env python3
# This file contains a command line client that can be used to access the API.

import sys
import os
import json
from optparse import OptionParser
import re

import importlib
sys.path.append(os.path.realpath('modules'))
client_module = importlib.import_module('RestApiClient')


# This is to modify the behaviour of the OptParser to make it check arguments
# more strictly
class NonCorrectingOptionParser(OptionParser):

    def _match_long_opt(self, opt):
        # Is there an exact match?
        if opt in self._long_opt:
            return opt
        else:
            self.error('"{0}" is not a valid command line option.'.format(opt))

# This method return the parser to parse our command line arguments.

USAGE_MESSAGE = "Type 'python apiclient.py --help' for usage."


def get_params(option, opt_str, value, parser):

    args = []
    next_opt = False
    while parser.rargs and not next_opt:
        if not parser.rargs[0].startswith('--'):
            args.append(parser.rargs.pop(0))
        else:
            next_opt = True

    setattr(parser.values, option.dest, args)


def get_parser():

    parser = NonCorrectingOptionParser(add_help_option=False)

    parser.add_option('-h', '--help', help='Show help message',
                      action='store_true')
    parser.add_option('--print_api',
                      help='Print all available endpoints of the API',
                      action='store_true')
    parser.add_option('-a', '--api', help='Path of the API to call. Required',
                      action='store')
    parser.add_option('-m', '--method',
                      help='HTTP method to call the API using, either GET, ' +
                           'POST, DELETE',
                      action='store', choices=['GET', 'POST', 'DELETE'])
    parser.add_option('--response_format',
                      help='Content-type of response, either ' +
                           'application/json, application/xml, ' +
                           'application/csv, or text/table. Defaults to json.',
                      action='store', default='application/json')
    parser.add_option('--request_format', '--content_type',
                      help='Content-type of body parameter. Required only ' +
                           'for endpoints that have \'body\' parameters.')
    parser.add_option('-v', '--version',
                      help='The version of the endpoint you would like to ' +
                           'use. Default is most recent version',
                      action='store')
    parser.add_option('--add_headers',
                      help='For any headers you would like to pass. This is ' +
                           'not required to use any endpoint. Must be in ' +
                           'format "<name1>=<value1>+<name2>=<value2>"')
    parser.add_option('-p', '--params',
                      help='For any parameters you would like to pass. ' +
                           'Individual parameters are separated by spaces.' +
                           '\nExample: --params <name1>="<value1>" ' +
                           '<name2>="<value2>"',
                      action='callback', callback=get_params, dest="params")
    parser.add_option('-r', '--range',
                      help='Allows you to construct a Range header to ' +
                           'perform paging (v3_0 endpoints and above only). ' +
                           'Range is 0 based inclusive, and must be in ' +
                           'formation \'x-y\'', action='store', default='')

    return parser

# This method takes the output of the /help/capabilities endpoint and prints it
# into a user readable format.


def print_api():

    api_client = client_module.RestApiClient()

    response = api_client.call_api('help/capabilities', 'GET')
    response_json = json.loads(response.read().decode('utf-8'))

    for category in response_json['categories']:
        for api in category['apis']:
            print("API: " + category['path'] + api['path'])
            print("Operations:")

            for operation in api['operations']:
                print("\tVersion: " + str(operation['version']))
                print("\tMethod: " + operation['httpMethod'])

                desc = re.sub("[\\t\\n\\r]+", " ", operation['description'])

                print("\tDescription: " + desc)

                sys.stdout.write("\tOutput Type(s): ")
                response_types = []
                for response_type in operation['supportedContentTypes']:
                    response_types.append(response_type['mimeType'])
                print(", ".join(response_types))
                print("\tParameters: ")

                for params in operation['parameters']:

                    print("\t\tName: " + params['name'])
                    if params['description']:
                        desc = re.sub("[\\t\\n\\r]+", " ",
                                      params['description'])
                        print("\t\tDescription: " + desc)

                    print("\t\tSource: " + params['source'])

                    print("\t\tRequired: " + str(params['required']))

                    for contentTypes in params['supportedContentTypes']:
                        try:
                            if contentTypes['dataType']:
                                print("\t\tType: " + contentTypes['dataType'])
                        except KeyError:
                            print("\t\tType: " + params['dataType'])
                        print("\t\tMimeType: " + contentTypes['mimeType'])
                        print("")

# This is the output when "apiclient.py -h" is called on the command line.


def print_help(parser):
    print(parser.format_help().strip())
    print("\n\nExample query: python apiclient.py --api /help/capabilities " +
          "--method GET --params httpMethods=\"['GET']\" " +
          "categories=\"['/help']\"\n\n")


def parse_params(args):

    params = {}
    if args:
        for x in args:
            key_value = x.split('=', 1)
            pair = {key_value[0]: key_value[1]}
            params.update(pair)
    return params

# This method calls the api for the user.


def make_request(args):

    # Create an API for the version specified by the user. If args.version is
    # None the latest version will be used.
    api_client = client_module.RestApiClient(version=args.version)

    # Make a copy of the headers so we are able to set some custom headers.
    headers = api_client.get_headers()

    # Gets endpoint from --api ENDPOINT argument
    endpoint = args.api

    # Strips endpoint of first forward slash, if it has one. Allows user to
    # supply or omit forward slash from beginning of endpoint.
    if str.startswith(endpoint, '/'):
        endpoint = endpoint[1:]

    # Changes 'Accept' header to --response_format RESPONSE_FORMAT argument.
    headers['Accept'] = args.response_format

    # This code snippet adds any extra headers you wish to send with your api
    # call. Must be in name1=value1+name2=value2 form.
    if args.add_headers:
        try:
            header_pairs = args.add_headers.split("+")
            for header_pair in header_pairs:
                header_pair = header_pair.split("=", 1)
                headers[header_pair[0]] = header_pair[1]
        except IndexError as ex:
            raise ParseError("Error: Parsing headers failed. Make sure " +
                             "headers are in format \"<name1>=<value1>+" +
                             "<name2>=<value2>\"", ex)

    if args.range:
        headers['Range'] = 'items='+args.range

    # This adds any query/body params to the list of query/body params.

    params = parse_params(args.params)

    # Checks content_type to see if it should send params as body param, or
    # query param.
    content_type = None

    # Gets Content-type from --request_format REQUEST_FORMAT argument.
    if args.request_format:
        headers['Content-type'] = args.request_format
        content_type = args.request_format

    try:
        # If content_type is application/json, then it is sending a JSON object
        # as a body parameter.
        if content_type == 'application/json':
            data = params['data'].encode('utf-8')
            return api_client.call_api(endpoint, 'POST', data=data,
                                       headers=headers)
        # Else it sends all params as query parameters.
        else:
            for key, value in params.items():
                params[key] = value
            return api_client.call_api(endpoint, args.method, params=params,
                                       headers=headers)

    except IndexError:
        raise ParseError('Error: Parameter parsing failed. Make sure any ' +
                         'parameters follow the syntax ' +
                         '<paramname>="<paramvalue>"')


def handle_response_error(response, body):

    try:
        response_json = json.loads(body)
        if response.code == 401:
            failed_auth()
        elif response.code == 422 and response_json['code'] == 36:
            print("\nFailed to parse Range header. The syntax of the " +
                  "--range parameter must follow 'x-y'.")
            print("Example: --range 0-1\n")
        return [response_json['code'], json.dumps(response_json, indent=2,
                separators=(',', ':'))]
    except ValueError:
        print("Failed to parse JSON of " + str(response.code) +
              " error response body")
        print("Text of Response Body: \n")
        return [None, body]


def failed_auth():
    print("AuthorizationError:")
    print("\nToken, or user credentials failed to authorize api call. " +
          "Please verify your token, or user credentials are correct.\n")
    print("Body returned by failed request:\n")


def main(args):

    # Then if --print_api is true, then apiclient prints output of
    # /help/capabilities endpoint.
    if args[0].print_api:
        print_api()
    # Then if --api and --method both have values, apiclient will attempt an
    # api request.
    elif args[0].api and args[0].method:
        # Gets response object from making api call.
        response = make_request(args[0])
        # Determines content type of response object (for printing).
        content_type = response.headers.get('Content-type')
        # Gleans body from response object.
        print(response.headers)
        body = response.read().decode('utf-8')
        output = body
        if response.code >= 300:
            # ERROR OCCURED, HANDLE ERROR
            [error_code, output] = handle_response_error(response, body)
        # SUCCESSFUL CALL
        # If JSON object, it pretty prints JSON
        # Else it merely prints the body of the response object.
        elif content_type == 'application/json':
            if body:
                try:
                    response_json = json.loads(body)
                    output = json.dumps(response_json, indent=2,
                                        separators=(',', ':'))
                except ValueError:
                    print("Failed to parse JSON, unparsed JSON below: ")
            else:
                print("\nResponse body was empty.\n")
        print(response.code)
        print("")
        print(output)

    # If either only api, or method args are sent, then then this error
    # message is printed.
    else:
        message = ""
        if args[0].api:
            message += "httpMethod must be specified by --method argument\n"
        if args[0].method:
            message += "api endpoint must be specified by --api argument\n"
        if message:
            print("ArgumentError: " + message)
        print(USAGE_MESSAGE+"\n")


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args[0].help:
        print_help(parser)
    elif not sys.argv[1:]:   # NO COMMAND LINE ARGUMENTS
        print(USAGE_MESSAGE+"\n")
    else:
        main(args)
