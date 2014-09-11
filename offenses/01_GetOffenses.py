# This sample demonstrates how to use the /siem/offenses endpoint in the
# REST API.

# For this scenario to work there must already be offenses on the system the
# sample is being run against.  The scenario demonstrates the following actions:
#  - How to get offenses.
#  - How to page through the results using the limit and offset parameters.
#  - How to filter the data that is returned with the fields parameter.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import json
import os
import sys
sys.path.append(os.path.realpath('../modules'))
from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities


def main():
    # Create our client.
    client = RestApiClient()

    # Using the /siem/offenses endpoint with a GET request.  Since no limit
    # parameter is provided, the first 20 offenses are retrieved from the
    # system.

    SampleUtilities.pretty_print_request(client, 'siem/offenses', 'GET')
    response = client.call_api('siem/offenses', 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve offense list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Display the number of offenses retrieved.
    response_body = json.loads(response.read().decode('utf-8'))
    print('Number of offenses retrived: ' + str(len(response_body)))

    # Display the content of an offense.

    SampleUtilities.pretty_print_request(client, 'siem/offenses?limit=1', 'GET')
    response = client.call_api('siem/offenses?limit=1', 'GET')
    SampleUtilities.pretty_print_response(response)

    # Paging offenses is useful when the user is expecting many results. Using
    # the /siem/offenses endpoint with a GET request, obtain offenses, 5 at a
    # time.

    # This is the number of offenses we want to retrieve at a time.
    limit = 5

    # This parameter indicates to retrieve offenses that start from the offset
    # value rather than from the beginning of the offenses. The first offense
    # has an offset of 0.  The default offset value is 0. In this loop, the
    # offset is incremented by the limit for each call to the offense API.
    offset = 0

    while True:

        # Retrieve some offenses.
        SampleUtilities.pretty_print_request(client,
                'siem/offenses?limit=' + str(limit) + '&offset=' + str(offset),
                'GET')
        response = client.call_api(
                'siem/offenses?limit=' + str(limit) + '&offset=' + str(offset),
                'GET')

        # Verify that the call to the API was successful.
        if (response.code != 200):
            print('Failed to retrieve offense list.')
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)

        # Increment the offset by limit so new offenses can be retrieved in the
        # next iteration of the loop.
        offset += limit

        response_body = json.loads(response.read().decode('utf-8'))

        number_of_offenses_retrieved = len(response_body)

        # Display number of offenses, and the IDs of the offenses retrieved.
        print(str(number_of_offenses_retrieved) + ' offenses were retrieved.')
        if (number_of_offenses_retrieved > 0):
            print("Offense IDs: ", end="")
            for offense in response_body:
                print(str(offense['id']) + ' ', end="")
            print()

        # If less than limit offenses were returned, then there are no more
        # offenses to be retrieved, exit the loop.
        if (number_of_offenses_retrieved < limit):
            break
        else:
            print()

        # If there are many offenses on the system, this loop could run for a
        # long time. If we have retrieved more than 50 offenses, then stop the
        # loop.
        if (offset > 50):
            break

    # Using the /siem/offenses endpoint with a GET request, filter the data that
    # is returned with the fields parameter. The fields parameter is a
    # comma-separated list of fields from the offense structure. Only the fields
    # that were requested are returned by the API.

    # Retrieve the id and status for the first 3 offenses.
    SampleUtilities.pretty_print_request(client,
        'siem/offenses?limit=3&fields=id,status', 'GET')
    response = client.call_api(
        'siem/offenses?limit=3&fields=id,status', 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve offense list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    SampleUtilities.pretty_print_response(response)

if __name__ == "__main__":
    main()
