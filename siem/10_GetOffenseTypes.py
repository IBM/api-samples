#!/usr/bin/env python3
# This sample demonstrates how to use the siem endpoint in the
# REST API.

# For this scenario to work, there must already be custom offense
# types on the system where the sample is being run.
# The scenario demonstrates the following
# actions:
#  - How to get all offense types
#  - How to get custom offense types
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # First we have to create our client
    client = client_module.RestApiClient(version='6.0')

    # -------------------------------------------------------------------------
    # Basic 'GET'
    # In this example we'll be using the GET endpoint of siem/offense_types
    # without any parameters. This will print absolutely everything
    # it can find, every parameter of every offense_type.

    # Send in the request
    SampleUtilities.pretty_print_request(client,
                                         'siem/offense_types',
                                         'GET')
    response = client.call_api('siem/offense_types', 'GET')

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    if (response.code != 200):
        print('Failed to retrieve the list of offense types')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Since the previous call had no parameters and response has a lot of text,
    # we'll just print out the number of offense_types
    response_body = json.loads(response.read().decode('utf-8'))
    print('Number of offense types retrived: ' + str(len(response_body)))

    # -------------------------------------------------------------------------
    # Using the fields parameter with 'GET'
    # If you just print out the result of a call to the siem/offense_types GET
    # endpoint there may be some fields displayed which you have no
    # interest in. Here, the fields parameter will make sure the only the
    # fields you want are displayed for each offense_type.

    # Setting a variable for all the fields that are to be displayed
    fields = '''id,database_type,name,custom'''

    # Send in the request
    SampleUtilities.pretty_print_request(client, 'siem/offense_types?fields=' +
                                         fields, 'GET')
    response = client.call_api('siem/offense_types?fields=' + fields, 'GET')

    # Once again, check the response code
    if (response.code != 200):
        print('Failed to retrieve list of offense types')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # This time we will print out the data itself
    SampleUtilities.pretty_print_response(response)

    # -------------------------------------------------------------------------
    # Using the filter parameter with 'GET'
    # Sometimes you'll want to narrow down your search to just a few
    # offense types. You can use the filter parameter to carefully
    # select what is returned after the call by the value of the fields.
    # Here we're only looking for custom offense types, as shown by
    # the value of 'custom' equal to 'true'.

    # Send in the request
    SampleUtilities.pretty_print_request(
        client, 'siem/offense_types?fields=' + fields + '&filter=custom=TRUE',
        'GET')
    response = client.call_api(
        'siem/offense_types?fields=' + fields + '&filter=custom=TRUE', 'GET')

    # Always check the response code
    if (response.code != 200):
        print('Failed to retrieve list of offense types')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # And output the data
    SampleUtilities.pretty_print_response(response)

    # -------------------------------------------------------------------------
    # Paging the 'GET' data using 'Range'
    # If you have a lot of offense types, then you may want to browse through
    # them just a few at a time. In that case, you can use the Range header to
    # limit the number of offense types shown in a single call.

    # In this example only custom offense types are retrieved.

    # Call the endpoint so that we can find how many
    # custom offense types there are.
    response = client.call_api('siem/offense_types?filter=custom=TRUE', 'GET')
    num_of_custom_offense_types = len(json.loads(response.read().
                                                 decode('utf-8')))

    # Copy the headers into our own variable
    range_header = client.get_headers().copy()

    # Set the starting point (indexing starts at 0)
    page_position = 0
    # and choose how many offense types you want to display at a time.
    offense_types_per_page = 5

    # Looping here in order to repeatedly show 5 offense types at a time
    # until we've seen all of the custom offense types or exit
    # character q is pressed
    input_string = ""
    while True:
        # Change the value for Range in the header in the format item=x-y
        range_header['Range'] = ('items=' + str(page_position) + '-' +
                                 str(page_position +
                                     offense_types_per_page - 1))

        # Send in the request
        SampleUtilities.pretty_print_request(
            client,
            'siem/offense_types?fields=' + fields + '&filter=custom=TRUE',
            'GET', headers=range_header)
        response = client.call_api(
            'siem/offense_types?fields=' + fields + '&filter=custom=TRUE',
            'GET',
            headers=range_header)

        # As usual, check the response code
        if (response.code != 200):
            print('Failed to retrieve list of offense types')
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)

        # Output the data
        SampleUtilities.pretty_print_response(response)

        # Check to see if all the offense types have been displayed
        if (page_position + offense_types_per_page >=
                num_of_custom_offense_types):
            print('All offense types have been printed to the screen.')
            break
        else:
            # Wait for the user to display the next set or quit
            input_string = input(
                'Push enter to bring up the next ' +
                str(offense_types_per_page) +
                ' offenses, or q to quit. ')
            # If the user entered the character 'q', quit.
            if (input_string == 'q'):
                break
            page_position += offense_types_per_page

if __name__ == "__main__":
    main()
