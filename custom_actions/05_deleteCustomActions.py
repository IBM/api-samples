#!/usr/bin/env python3
# This sample demonstrates how to use various DELETE /custom_actions/ endpoints
# REST API.
#
# This sample will delete all custom action scripts and custom actions
# from the system. It is recommended that it is not run on a production system.
#
# The scenario demonstrates the following actions:
#  - Deleting custom action scripts
#  - Deleting custom actions

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
    # Endpoints used in this sample
    actions_endpoint = 'analytics/custom_actions/actions'
    scripts_endpoint = 'analytics/custom_actions/scripts'

    # Retrieving collections of actions currently stored.
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
    # Extracting actions
    actions = json.loads(response.read().decode('utf-8'))

    # Retrieving collections of scripts currently stored.
    SampleUtilities.pretty_print_request(restClient,
                                         scripts_endpoint,
                                         'GET')
    response = restClient.call_api(scripts_endpoint,
                                   'GET')
    # Verify that the call was successful.
    if (response.code != 200):
        print('Failed to retrieve custom action list')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Extracting scripts
    scripts = json.loads(response.read().decode('utf-8'))

    actions_count = len(actions)
    scripts_count = len(scripts)
    # Print count of collections.
    print("Custom actions retrieved: " + str(actions_count))
    print("Custom action scripts retrieved: " + str(scripts_count))
    print()

    # Deleting custom actions first as scripts cannot be deleted
    # while tied in use with a custom action.

    # Accept header for DELETE endpoints.
    headers = {'Accept': 'text/plain'}

    if actions_count > 0:
        print('Deleting [{0}] custom actions.\n'
              .format(str(actions_count)))
        # Iterating over each action and calling the DELETE endpoint.
        for action in actions:
            # Extracting the custom action id.
            action_id = str(action['id'])
            delete_endpoint = actions_endpoint + '/' + action_id
            SampleUtilities.pretty_print_request(restClient,
                                                 delete_endpoint,
                                                 'DELETE')
            # Calling DELETE endpoint.
            response = restClient.call_api(delete_endpoint,
                                           'DELETE',
                                           headers=headers)
            # Verify that DELETE was successful.
            if response.code != 204:
                print('Failed to delete custom action ' + action_id)
                SampleUtilities.pretty_print_response(response)
                exit(1)
            else:
                print(action_id + ' successfully deleted\n')
    else:
        print('No custom actions found to delete.')

    if scripts_count > 0:
        print('Deleting [{0}] custom action scripts\n'
              .format(str(scripts_count)))
        # Iterating over each script and calling the DELETE endpoint.
        for script in scripts:
            # Extracting the script id
            script_id = str(script['id'])
            delete_endpoint = scripts_endpoint + '/' + script_id
            SampleUtilities.pretty_print_request(restClient,
                                                 delete_endpoint,
                                                 'DELETE')
            # Calling DELETE endpoint.
            response = restClient.call_api(delete_endpoint,
                                           'DELETE',
                                           headers=headers)
            # Verify that DELETE was successful.
            if response.code != 204:
                print('Failed to delete script ' + action_id)
                SampleUtilities.pretty_print_response(response)
                exit(1)
            else:
                print(script_id + ' successfully deleted\n')
    else:
        print('No custom action scripts found to delete.')

if __name__ == '__main__':
    main()
