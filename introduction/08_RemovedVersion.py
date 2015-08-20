#!/usr/bin/env python3
# This sample demonstrates the Removed response message. The Removed
# response message is returned for each request to a removed API endpoint.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # First we have to create our client
    # Version 1.0 is a remved version of the API
    client = client_module.RestApiClient(version='1.0')

    # Call the API with a removed version.
    SampleUtilities.pretty_print_request(client,
                                         'referencedata/sets',
                                         'GET')
    response = client.call_api('referencedata/sets', 'GET')

    # Since we called a removed version of the API we expect the Removed
    # response message to be set.
    response_body = response.read().decode('utf-8')
    if response.code == 422 and 'has been removed' in response_body:

        print("The response has a Removed message. This is the content of "
              "the response message:\n")
        print(response.code)
        parsed_response = json.loads(response_body)
        print(json.dumps(parsed_response, indent=4))

    else:

        print("The response did not have a Removed message.")


if __name__ == "__main__":
    main()
