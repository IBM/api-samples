#!/usr/bin/env python3
# This sample demonstrates how to use the /qvm/saved_searches endpoint
# in the REST API.

# - The scenario demonstrates the following actions:
#    - How to get available saved searches.

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
    client = client_module.RestApiClient(version='6.0')

    # Using the /qvm/saved_searches endpoint with a GET request.
    saved_searches_endpoint_url = 'qvm/saved_searches'
    SampleUtilities.pretty_print_request(client, saved_searches_endpoint_url,
                                         'GET')
    response = client.call_api(saved_searches_endpoint_url, 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve saved search list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Display the number of saved searches retrieved.
    response_body = json.loads(response.read().decode('utf-8'))
    number_of_searches_retrieved = len(response_body)

    # Pretty print response
    print(str(number_of_searches_retrieved) +
          ' saved searches were retrieved.\n')
    print('Available QVM Saved Searches:')
    print(json.dumps(response_body, indent=2))

if __name__ == "__main__":
    main()
