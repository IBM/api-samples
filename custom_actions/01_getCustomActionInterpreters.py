#!/usr/bin/env python3
# This sample demonstrates how to use the GET analytics/custom_actions
# /interpreters endpoint in the REST API.

# The scenario demonstrates the following actions:
#  - How to get all custom action interpreters.
#  - How to retrieve specific custom action interpreters.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/endpoints endpoint.
import json
import sys
import os

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Create our client.
    restClient = client_module.RestApiClient(version='6.0')
    # Endpoint used in this sample.
    interpreter_endpoint = 'analytics/custom_actions/interpreters'
    # Using the analytics/custom_actions/interpreters
    # endpoint with GET request.
    SampleUtilities.pretty_print_request(restClient,
                                         interpreter_endpoint,
                                         'GET')
    # Getting collection of available interpreters.
    response = restClient.call_api(interpreter_endpoint, 'GET')
    # Checking for a successful response code.
    if (response.code != 200):
        print('Failed to retrieve custom action interpreter list')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)
    # Extracting interpreters from response.
    response_body = json.loads(response.read().decode('utf-8'))
    total_retrieved = len(response_body)
    # Print total interpreters received.
    print(str(total_retrieved) +
          ' custom action interpreters were retrieved')

    interpreter_id = None

    if (total_retrieved > 0):

        print("Retrieved interpreters:\n")
        format_str = 'id=[{0}], name=[{1}]'
        # Iterating over retrieved interpreters.
        for interpreter in response_body:
            inter_id = str(interpreter['id'])
            inter_name = str(interpreter['name'])

            print(format_str.format(inter_id, inter_name))
            interpreter_id = inter_id

        print()

    # Demonstrating getting specific custom action interpreters using
    # an id retrieved from the previous call.
    if (interpreter_id is not None):
        # Appending interpreter endpoint with id received earlier.
        interpreter_endpoint += '/' + interpreter_id
        SampleUtilities.pretty_print_request(restClient,
                                             interpreter_endpoint,
                                             'GET')
        # Getting specific interpreter
        response = restClient.call_api(interpreter_endpoint,
                                       'GET')
        # Checking for a successful response code.
        if (response.code != 200):
            print('Failed to retrieve custom action interpreter with id ' +
                  interpreter_id)
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)
        # Extracting interpreter from response.
        response_body = json.loads(response.read().decode('utf-8'))
        print('Successfully retrieved custom action interpreter with id ' +
              str(response_body['id']))

if __name__ == "__main__":
    main()
