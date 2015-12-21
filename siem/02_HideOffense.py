#!/usr/bin/env python3
# This sample demonstrates how to use the siem endpoint in the
# REST API.

# This sample is interactive.

# For this scenario to work there must already be offenses on the system the
# sample is being run against.
# THIS SAMPLE WILL MAKE CHANGES TO THE OFFENSE IT IS RUN AGAINST
# The scenario demonstrates the following actions:
#  - How to get offenses with the status OPEN using the filter parameter
#  - How to get a single offense given the ID
#  - How to decode data received and access the information
#  - How to hide an offense

# To view a list of the endpoints with the parameters they accept, you can view
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
    client = client_module.RestApiClient(version='5.0')

    # Send in the request to GET all the OPEN offenses, but only showing some
    # of the fields, enough to distinguish the offenses.
    SampleUtilities.pretty_print_request(
        client, 'siem/offenses?fields=id,description,status,offense_type,' +
        'offense_source&filter=status=OPEN', 'GET')
    response = client.call_api(
        'siem/offenses?fields=id,description,status,offense_type,' +
        'offense_source&filter=status=OPEN', 'GET')

    # Print out the result
    SampleUtilities.pretty_print_response(response)

    if (response.code != 200):
        print('Call Failed')
        sys.exit(1)

    # Prompt the user for an ID
    offense_ID = input(
        'Select an offense to hide. Please type its ID or quit. ')

    # Error checking because we want to make sure the user has selected an OPEN
    # offense.
    while True:

        if (offense_ID == 'quit'):
            exit(0)

        # Make the request to 'GET' the offense chosen by the user
        SampleUtilities.pretty_print_request(client, 'siem/offenses/' +
                                             str(offense_ID), 'GET')
        response = client.call_api('siem/offenses/' + str(offense_ID), 'GET')

        # Save a copy of the data, decoding it into a string so that
        # we can read it
        response_text = response.read().decode('utf-8')

        # Check response code to see if the offense exists
        if (response.code == 200):

            # Reformat the data string into a dictionary so that we
            # easily access the information.
            response_body = json.loads(response_text)
            # Ensure the offense is OPEN
            if (response_body['status'] != 'OPEN'):
                offense_ID = input('The offense you selected is not OPEN. ' +
                                   'Please try again or type quit. ')
            else:
                # Only breaks when the ID exists and is OPEN
                break
        else:
            offense_ID = input('An offense by that ID does not exist. ' +
                               'Please try again or type quit. ')

    # Prints the response, which has already been decoded.
    # **Only works on responses that have been decoded**
    print(json.dumps(response_body, indent=4))

    while True:
        # As this sample uses data on your system, ensure that the user wants
        # to hide the offense.
        confirmation = input(
            'Are you sure you want to hide this offense? ' +
            'This will affect the status of the offense. (YES/no)\n')

        if (confirmation == 'YES'):

            # Sends in the POST request to update the offense. Also using
            # fields to trim down the data received by POST.
            SampleUtilities.pretty_print_request(
                client, 'siem/offenses/' + offense_ID +
                '?status=HIDDEN&fields=id,description,status,' +
                'offense_type,offense_source', 'POST')
            response = client.call_api(
                'siem/offenses/' + offense_ID + '?status=HIDDEN' +
                '&fields=id,description,status,offense_type,offense_source',
                'POST')

            # Prints the data received by POST
            SampleUtilities.pretty_print_response(response)

            if (response.code != 200):
                print('Call Failed')
                SampleUtilities.pretty_print_response(response)
                sys.exit(1)

            print('Offense ' + offense_ID + ' hidden')
            break
        elif (confirmation == 'no'):
            print('You have decided not to hide offense ' + offense_ID +
                  '. This sample will now end.')
            break

        else:
            print(confirmation + ' is not a valid response.')


if __name__ == "__main__":
    main()
