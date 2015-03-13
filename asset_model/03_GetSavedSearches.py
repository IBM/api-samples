#!/usr/bin/env python3
# This sample demonstrates how to use the /asset_model/saved_searches endpoint
# in the REST API.

# - The scenario demonstrates the following actions:
#    - How to get available saved searches.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import sys
import os
sys.path.append(os.path.realpath('../modules'))
import json
from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities


def main():
    # Create our client.
    client = RestApiClient(version='3.0')

    # Using the /asset_model/savedsearches endpoint with a GET request.
    SampleUtilities.pretty_print_request(client, 'asset_model/saved_searches',
                                         'GET')
    response = client.call_api('asset_model/saved_searches', 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve saved search list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Display the number of saved searches retrieved.
    response_body = json.loads(response.read().decode('utf-8'))
    number_of_searches_retrieved = len(response_body)

    # Display number of searches, and the names of the searches retrieved.
    print(str(number_of_searches_retrieved) +
          ' saved searches were retrieved.')
    if (number_of_searches_retrieved > 0):
        print("Saved Search Names: ", end="")
        for asset in response_body:
            print(str(asset['name']) + ', ', end="")
        print()

if __name__ == "__main__":
    main()
