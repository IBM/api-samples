#!/usr/bin/env python3
# This sample demonstrates how to use the siem endpoint in the
# REST API.

# This sample is interactive.

# In this scenario we will be closing an offense in a system similar to how the
# the user can close offenses in the UI. This has four main processes.
# 1. Select an offense
# 2. Select a closing_reason_id
# 3. Modify Status to CLOSED
# 4. Leave a note

# For this scenario to work there must already be offenses on the system the
# sample is being run against.
# THIS SAMPLE WILL MAKE CHANGES TO THE OFFENSE IT IS RUN AGAINST
# The scenario demonstrates the following actions:
#  - Using filter and field parameters with GET endpoints to GET a
#    comprehensive list
#  - Selecting objects with GET from known lists of things with specific
#    properties
#  - How to post notes on an offense
#  - How to close an offense

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

    # Send in the request to show all offenses. Here we're using the fields
    # parameter so that we only see the important information about the
    # offenses, and using the filter parameter so that we only get offenses
    # that aren't already closed.
    SampleUtilities.pretty_print_request(
        client, 'siem/offenses?fields=id,description,status,offense_type,' +
        'offense_source&filter=status!=CLOSED', 'GET')
    response = client.call_api(
        'siem/offenses?fields=id,description,status,offense_type,' +
        'offense_source&filter=status!=CLOSED', 'GET')

    # Print out the result
    SampleUtilities.pretty_print_response(response)

    # Don't forget to check the response code
    if (response.code != 200):
        print('Call Failed')
        sys.exit(1)

    # Prompt the user for an offense ID
    offense_ID = input(
        'Select an offense to close. Please type its ID or quit. ')

    # Error checking because we want to make sure the user has selected an
    # OPEN or HIDDEN offense.
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
            # Ensure the offense is OPEN or HIDDEN
            if (response_body['status'] == 'CLOSED'):
                offense_ID = input(
                    'The offense you selected is already CLOSED. ' +
                    'Please try again or type quit. ')
            else:
                # Only breaks when the ID exists and not CLOSED
                break
        else:
            offense_ID = input(
                'An offense by that ID does not exist. ' +
                'Please try again or type quit. ')

    # Print out the info about the offense the user wants to close
    # **Only works on things already decoded**
    print(json.dumps(response_body, indent=4))

    # Now since we're closing an offense, we need a closing reason to justify
    # closing the offense. While both the status parameter and the
    # closing_reason_id parameters are optional, they're dependent on one
    # another, so if you close an offense you NEED to give a reason, and vice
    # versa.

    # Here we're showing the user what options they have when selecting a
    # closing_reason so send in the request.
    SampleUtilities.pretty_print_request(client,
                                         'siem/offense_closing_reasons', 'GET')
    response = client.call_api('siem/offense_closing_reasons', 'GET')
    # And print out the response
    SampleUtilities.pretty_print_response(response)

    # Always check the response code
    if (response.code != 200):
        print('Call Failed')
        sys.exit(1)

    # Now that the user has seen which closing_reasons there are to choose
    # from, have them select one.
    closing_reason_ID = input('Please select a closing reason or type quit. ')

    while True:
        if (closing_reason_ID == 'quit'):
            exit(0)

        # Call the API to see if we can GET it, seeing if it exists
        SampleUtilities.pretty_print_request(
            client, 'siem/offense_closing_reasons/' + closing_reason_ID, 'GET')
        response = client.call_api('siem/offense_closing_reasons/' +
                                   closing_reason_ID, 'GET')

        if (response.code == 200):
            # Breaks the loop once the closing reason exists.
            break

        closing_reason_ID = input(
            'There has been an error. Please try again or type quit. ')

    # Now that we've selected which offense and which closing_reason we want to
    # close, we need have the option of leaving a note. This is to reflect the
    # UI. In the UI when you decide to close an offense, you have option to
    # leave a note usually giving further information than the closing_id

    make_note = input(
        'Do you want to create a note for this offense? (YES/no) ')
    if (make_note == 'YES'):
        # Quote some text for the not to contain
        note_text = input('Please enter a note to close the offense with:\n')
        while True:
            if note_text != '':
                confirmation = input(
                    'Are you sure you want to enter the note "' + note_text +
                    '"? (YES/no) ')
                if (confirmation == 'YES'):
                    break
            note_text = input(
                'Please enter a note to close the offense with:\n')

    # Ensure that the user really wants to close the offense
    while True:
        confirm = input(
            'Are you sure you want to close offense ' + offense_ID +
            ' with closing reason ' + closing_reason_ID + '? (YES/no)\n')

        if (confirm == 'YES'):
            break
        elif (confirm == 'no'):
            print('Not closing offense ' + offense_ID)
            exit(0)
        else:
            print(confirm + ' is not a valid response.')

    # Once the user has confirmed they want to close the offense, we can start
    # updating the offense

    # First let's create the note (if the user wants to)
    if (make_note == 'YES'):
        params = {'note_text': note_text}
        response = client.call_api('siem/offenses/' + offense_ID + '/notes',
                                   'POST', params=params, print_request=True)

        SampleUtilities.pretty_print_response(response)

        if (response.code != 201):
            print('Call Failed Creating Note')
            exit(1)

    # Then we change the status to CLOSED and add a closing reason. Also using
    # fields to trim down the data received by POST.
    SampleUtilities.pretty_print_request(
        client, 'siem/offenses/' + offense_ID +
        '?status=CLOSED&closing_reason_id=' + closing_reason_ID +
        '&fields=id,description,status,offense_type,offense_source', 'POST')
    response = client.call_api(
        'siem/offenses/' + offense_ID + '?status=CLOSED&closing_reason_id=' +
        closing_reason_ID +
        '&fields=id,description,status,offense_type,offense_source', 'POST')

    # Display it at the end to make sure nothing messed up
    SampleUtilities.pretty_print_response(response)

    if response.code != 200:
        print('Call Failed Closing Item')

    print('Offense closed')

if __name__ == "__main__":
    main()
