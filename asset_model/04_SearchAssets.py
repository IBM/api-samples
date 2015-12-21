#!/usr/bin/env python3
# This sample demonstrates how to use the
# /asset_model//saved_searches/{saved_search_id}/results endpoint in the REST
# API.

# - For this scenario to work there must already be assets on the system the
# - sample is being run against.  The scenario demonstrates the following
#   actions:
#    - How to get available saved searches.
# - How to use a saved search against assets.

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
    client = client_module.RestApiClient(version='5.0')

    # Using the /asset_model/properties endpoint with a GET request.
    SampleUtilities.pretty_print_request(client, 'asset_model/saved_searches',
                                         'GET')
    response = client.call_api('asset_model/saved_searches', 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve saved searches list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Find the number of saved searches retrieved.
    response_body = json.loads(response.read().decode('utf-8'))
    number_of_searches_retrieved = len(response_body)

    # Display number of searches, and the names of the searches retrieved.
    print(str(number_of_searches_retrieved) + ' searches were retrieved.\n')
    if (number_of_searches_retrieved > 0):
        print("Searching Assets...\n\n")
        for search in response_body:
            # Retrieve the saved search unique identifier.
            saved_search_id = str(search['id'])
            saved_search_name = str(search['name'])

            print('Running saved search : ' + saved_search_name)

            # Using the /asset_model/saved_searches/{saved_search_id}/results
            # endpoint with a GET request.
            search_endpoint_url = ('asset_model/saved_searches/' +
                                   saved_search_id + '/results')
            SampleUtilities.pretty_print_request(client, search_endpoint_url,
                                                 'GET')
            search_response = client.call_api(search_endpoint_url, 'GET')

            if(response.code != 200):
                print("Failed to search assets.")
                SampleUtilities.pretty_print_response(response)
                sys.exit(1)

            # Find the number of assets found
            search_response_body = json.loads(search_response.read().
                                              decode('utf-8'))
            number_of_assets_found = len(search_response_body)

            # Display the number of assets retrieved.
            print(str(number_of_assets_found) + ' assets were retrieved.\n')
        print()

if __name__ == "__main__":
    main()
