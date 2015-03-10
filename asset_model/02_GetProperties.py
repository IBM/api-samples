#!/usr/bin/env python3
# This sample demonstrates how to use the /asset_model/properties endpoint in the
# REST API.

# - The scenario demonstrates the following actions:
#   - How to get available asset properties.	

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import sys, os
sys.path.append(os.path.realpath('../modules'))
import json
from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities

def main():
    # Create our client.
    client = RestApiClient(version='3.0')

    # Using the /asset_model/properties endpoint with a GET request. 
    SampleUtilities.pretty_print_request(client, 'asset_model/properties', 'GET')
    response = client.call_api('asset_model/properties', 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve propertiy list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Display the number of properties retrieved.
    response_body = json.loads(response.read().decode('utf-8'))
    number_of_properties_retrieved = len(response_body)
		
    # Display number of properties, and the names of the properties retrieved.
    print(str(number_of_properties_retrieved) + ' properties were retrieved.')
    if (number_of_properties_retrieved > 0):
        print("Property Names: ", end="")
        for property in response_body:
            print(str(property['name']) + ', ', end="")
        print()		

if __name__ == "__main__":
    main()
