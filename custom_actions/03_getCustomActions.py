#!/usr/bin/env python3
# This sample demonstrates how to use the GET analytics/custom_actions/actions
# endpoint in the REST API.

# For this scenario to work there must already be custom actions on the system
# the sample is being run against.  The scenario demonstrates the following
# actions:
#  - How to get all custom actions.
#  - How to retrieve specific custom actions

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import sys
import os
import json

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Create our client.
    restClient = client_module.RestApiClient(version='5.0')
    # Endpoint used in this endpoint.
    actions_endpoint = 'analytics/custom_actions/actions'
    # Using the analytics/custom_actions/actions endpoint with GET request.
    SampleUtilities.pretty_print_request(restClient,
                                         actions_endpoint,
                                         'GET')
    response = restClient.call_api(actions_endpoint,
                                   'GET')

    # Verify that the call was successful.
    if (response.code != 200):
        print('Failed to retrieve custom action list')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    response_body = json.loads(response.read().decode('utf-8'))
    total_retrieved = len(response_body)

    print(str(total_retrieved) + ' custom actions were retrieved')

    action_id = None

    if (total_retrieved > 0):

        print("Received custom actions:")
        format_str = 'id=[{0}], name=[{1}], param count=[{2}]\n'
        for action in response_body:
            received_id = str(action['id'])
            received_name = action['name']
            param_count = str(len(action['parameters']))
            print(format_str.format(received_id, received_name, param_count))
            # Setting value for use later with /actions/{id} endpoint.
            action_id = received_id
        print()

    # Demonstrating getting specific custom action using an id
    # retrieved from the previous call
    if (action_id is not None):
        actions_endpoint += '/' + action_id
        SampleUtilities.pretty_print_request(restClient,
                                             actions_endpoint,
                                             'GET')
        # Calling API endpoint to get specific custom action
        response = restClient.call_api(actions_endpoint,
                                       'GET')
        # Checking for a successful response code
        if (response.code != 200):
            print('Failed to retrieve custom action with id ' + action_id)
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)

        response_body = json.loads(response.read().decode('utf-8'))
        response_id = str(response_body['id'])
        print('Successfully retrieved custom action with id ' + response_id)

    else:
        # No custom actions found to use with the GET /actions/{id} endpoint
        print('No available custom actions found to demonstrate'
              ' /actions/{id} endpoint.')

if __name__ == "__main__":
    main()
