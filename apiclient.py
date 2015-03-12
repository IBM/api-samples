#This file contains a command line client that can be used to access the API.

import sys, os
sys.path.append(os.path.realpath('modules'))
import json
from RestApiClient import RestApiClient
from optparse import OptionParser
from optparse import BadOptionError
from optparse import AmbiguousOptionError
import re
try:
    import urllib.parse as urlparse
except ImportError:
    import urllib as urlparse

# This is to modify the behaviour of the OptParser to make it behave more like
# argparse. Ignore.
class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    When unknown arguments are encountered, bundle with largs and try again,
    until rargs is depleted.  

    sys.exit(status) will still be called if a known argument is passed
    incorrectly (e.g. missing arguments or bad argument types, etc.)        
    """
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self,largs,rargs,values)
            except (BadOptionError,AmbiguousOptionError) as e:
                largs.append(e.opt_str)

# This method return the parser to parse our command line arguments.

def get_parser():

    parser = PassThroughOptionParser(add_help_option=False)
    parser.add_option('-h', '--help', help='Show help message', action='store_true')
    parser.add_option('--print_api', help='Print all available endpoints of the API', action='store_true')
    parser.add_option('--api', help='Path of the API to call. Required', action='store')
    parser.add_option('--method', help='HTTP method to call the API using, either GET, POST, DELETE', action='store', choices=['GET', 'POST', 'DELETE'])
    parser.add_option('--output', help='Output format, either application/json, application/xml, application/csv, or text/table. Defaults to json.', action='store', default='application/json')
    parser.add_option('--content_type', help='Content-type of body parameter. Required only for endpoints that have \'body\' parameters.')
    parser.add_option('--ver', help='The version of the endpoint you would like to use. Default is most recent version', action='store')
    parser.add_option('--add_headers', help='For any headers you would like to pass. This is not required to use any endpoint. Must be in format "<name1>=<value1>+<name2>=<value2>"')
    
    return parser

# This method takes the output of the /help/capabilities endpoint and prints it
# into a user readable format.

def print_api(settings):

    settings['version'] = None
    api_client = RestApiClient(settings)

    response = api_client.call_api('help/capabilities', 'GET')
    response_json = json.loads(response.read().decode('utf-8'))

    for category in response_json['categories']:
        for api in category['apis']:
            print("API: " + category['path'] + api['path'])
            print("Operations:")

            for operation in api['operations']:
                print("\tVersion: " + str(operation['version']))
                print("\tMethod: " + operation['httpMethod'])

                desc = re.sub("[\\t\\n\\r]+"," ", operation['description'])

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
                        desc = re.sub("[\\t\\n\\r]+"," ", params['description'])
                        print("\t\tDescription: " + desc)

                    print ("\t\tSource: " + params['source'])

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
    print("""  --<parameter_name>="<parameter_value>"
                   Any query parameters must be in this format. 
                   Ex. name="example"

Example query: python apiclient.py --api /help/capabilities --method GET --httpMethods="['POST']" --ver="1.0" 

""")

# This method calls the api for the user.

def make_request(args):

    # Create an API for the version specified by the user. If args.version is
    # None the latest version will be used.
    api_client = RestApiClient(version=args[0].ver)

    # Gets endpoint from --api ENDPOINT argument
    endpoint = args[0].api

    # Strips endpoint of first forward slash, if it has one. Allows user to 
    # supply or omit forward slash from beginning of endpoint.
    if str.startswith(endpoint, '/'):
        endpoint = endpoint[1:]

    # Make a copy of the headers so we are able to set some custom headers.
    headers = api_client.get_headers()

    # Changes 'Accept' header to --response_format RESPONSE_FORMAT argument.
    headers['Accept'] = args[0].output

    # This code snippet adds any extra headers you wish to send with your api 
    # call. Must be in name1=value1+name2=value2 form.
    if args[0].add_headers:
        header_pairs = args[0].add_headers.split("+")
        for header_pair in header_pairs:
            header_pair = header_pair.split("=")
            headers[header_pair[0]] = header_pair[1]

    # This adds any query/body params to the list of query/body params.
    params = {}
    for x in range(1, len(args[1]), 2):
        name_value = {args[1][x-1][2:]: args[1][x]}
        params.update(name_value)
 
    # Checks content_type to see if it should send params as body param, or 
    # query param.
    content_type = None

    # Gets Content-type from --content_type CONTENT_TYPE argument.
    if args[0].content_type:
        headers['Content-type'] = args[0].content_type
        content_type = args[0].content_type

    # If content_type is application/json, then it is sending a JSON object as
    # a body parameter.
    try:
        if content_type == 'application/json':
            data = params['data'].encode('utf-8')
            return api_client.call_api(endpoint, 'POST', headers=headers, data=data)
    # Else it sends all params as query parameters.
        else:
            for key, value in params.items():
                params[key] = urlparse.quote(value)
            return api_client.call_api(endpoint, args[0].method, headers=headers, params=params)
              
    except IndexError:
        raise Exception('Parameter parsing failed. Make sure any parameters follow the syntax --<paramname>="<paramvalue>"')

    

def main():

    # Gets parser to parse args.
    parser = get_parser()
    args = parser.parse_args()

    # If -h, --help is true. Prints api help.
    if args[0].help:
        print_help(parser)
    # Then if --print_api is true, then apiclient prints output of /help/capabilities
    # endpoint.
    elif args[0].print_api:
        print_api(settings)
    # Then if --api and --method both have values, apiclient will attempt an api request.
    elif args[0].api and args[0].method:
        # Gets response object from making api call.
        response = make_request(args)
        # Determines content type of response object (for printing).
        content_type = response.headers.get('Content-type')
        # Gleans body from response object.
        body = response.read().decode('utf-8')

        # If JSON object, it pretty prints JSON
        # Else it merely prints the body of the response object.
        if content_type == 'application/json':
            response_json = json.loads(body)
            print(json.dumps(response_json, indent=2, separators=(',', ':')))
        else:
            print(body)
    # If no args or incomplete args are sent, then print_help(parser) is called.
    else:
        message = ""
        if args[0].api:
            message += "httpMethod must be specified by --method argument\n"
        if args[0].method:
            message += "api endpoint must be specified by --api argument\n"
        if message:
            print("ArgumentError: " + message)
        print("Type 'python apiclient.py --help' for usage.\n")
            


if __name__ == "__main__":
    main()
