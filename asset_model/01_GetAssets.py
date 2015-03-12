# This sample demonstrates how to use the /asset_model/assets endpoint in the
# REST API.

# For this scenario to work there must already be assets on the system the
# sample is being run against.  The scenario demonstrates the following actions:
#  - How to get assets.

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
    client = RestApiClient(version='2.0')

    # Using the /asset_model/assets endpoint with a GET request. 
    SampleUtilities.pretty_print_request(client, 'asset_model/assets', 'GET')
    response = client.call_api('asset_model/assets', 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve asset list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Display the number of assets retrieved.
    response_body = json.loads(response.read().decode('utf-8'))
    number_of_assets_retrieved = len(response_body)
		
    # Display number of assets, and the IDs of the assets retrieved.
    print(str(number_of_assets_retrieved) + ' assets were retrieved.')
    if (number_of_assets_retrieved > 0):
        print("Asset IDs: ", end="")
        for asset in response_body:
            print(str(asset['id']) + ' ', end="")
        print()		

if __name__ == "__main__":
    main()
