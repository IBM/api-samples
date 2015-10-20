#!/usr/bin/env python3
# This sample demonstrates how to use the GET analytics/custom_actions/scripts
# endpoint in the REST API.

# For this scenario to work there must already be custom action scripts on the
# system the sample is being run against.
# The scenario demonstrates the following actions:
#  - How to get all custom action scripts
#  - How to retrieve specific custom action scripts

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import sys
import os
import json

sys.path.append(os.path.realpath('../modules'))
from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities


def main():
    # Create our client.
    restClient = RestApiClient(version='5.0')
    # Endpoint used in this sample.
    scripts_endpoint = 'analytics/custom_actions/scripts'
    # Using the analytics/custom_actions/scripts endpoint with GET request.
    SampleUtilities.pretty_print_request(restClient,
                                         scripts_endpoint,
                                         'GET')
    # Calling endpoint to get all available scripts.
    response = restClient.call_api(scripts_endpoint, 'GET')

    # Checking for a successful response code.
    if (response.code != 200):
        print('Failed to retrieve custom action script list')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)
    # Extract the script metadata from the response.
    response_body = json.loads(response.read().decode('utf-8'))
    total_retrieved = len(response_body)
    # Print total received
    print(str(total_retrieved) + ' custom action scripts were retrieved')

    script_id = None

    if (total_retrieved > 0):

        print('Retrieved scripts:\n')
        format_str = 'id=[{0}], file name=[{1}]'
        # Iterating over each script received.
        for script in response_body:

            retrieved_id = str(script['id'])
            file_name = str(script['file_name'])

            print(format_str.format(retrieved_id, file_name))
            # Setting for use later with the /scripts/{id}
            # endpoint.
            script_id = script['id']

        print()

    # Demonstrating getting specific scripts using
    # an id retrieved from the previous call.
    if (script_id is not None):
        scripts_endpoint += '/' + str(script_id)
        SampleUtilities.pretty_print_request(restClient,
                                             scripts_endpoint,
                                             'GET')
        response = restClient.call_api(scripts_endpoint,
                                       'GET')
        # Checking for a successful response code.
        if (response.code != 200):
            print('Failed to retrieve custom action script with id ' +
                  script_id)
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)
        # Extracting script from response.
        response_body = json.loads(response.read().decode('utf-8'))
        received_id = response_body['id']
        print('Successfully retrieved custom action script with id ' +
              str(received_id))

    else:
        print('No available scripts found to demonstrate'
              'the GET /scripts/{id} endpoint.')

if __name__ == "__main__":
    main()
