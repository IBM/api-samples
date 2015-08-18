#!/usr/bin/env python3
# In this example we will see how data in reference maps can be manipulated
# using the REST API.

# Our organization has several secure servers that can only be accessed by
# security administrators. These administrators can only access these servers
# during their scheduled shift and only one administrator is ever on duty for a
# single server at one time (although one administrator can supervise several
# servers at once). Furthermore some servers are not used during some shifts
# and so should not be accessed at all during this time.

# Our human resources system tracks the shift schedule of our security
# administrators and maintains a list of the servers that each one is
# supervising. We would like to use this information to generate offenses if
# any of these servers are improperly accessed.

# We have already created a reference data map on our system that matches the
# ip addresses of our servers to the user names of the administrators that can
# access them. We have also created a rule that generates an offense if any
# access is made to the servers by users not in the reference map.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Create our client and set up some sample data.
    client = client_module.RestApiClient(version='5.0')
    setup_data(client)

    # First lets see who is on duty now.
    print("These administrators are on duty during the first shift:")
    response = client.call_api(
        'reference_data/maps/rest_api_samples_current_admin_shift', 'GET')
    SampleUtilities.pretty_print_response(response)

    # # Change to the second shift as scheduled by our HR system.

    # Get the current shift.
    response = client.call_api(
        'reference_data/maps/rest_api_samples_current_admin_shift', 'GET')
    response_body = json.loads(response.read().decode('utf-8'))
    data = response_body['data']

    # Change to the second shift.
    print("Changing to the second shift:")
    update_reference_map(get_second_shift_schedule_from_hr(), data, client)
    # Show that the change has happened.
    response = client.call_api(
        'reference_data/maps/rest_api_samples_current_admin_shift', 'GET')
    SampleUtilities.pretty_print_response(response)

    # # Change to the third shift as scheduled by our HR system.

    # Get the current shift.
    response = client.call_api(
        'reference_data/maps/rest_api_samples_current_admin_shift', 'GET')
    response_body = json.loads(response.read().decode('utf-8'))
    data = response_body['data']

    # Change to the third shift.
    print("Changing to the third shift:")
    update_reference_map(get_third_shift_schedule_from_hr(), data, client)
    # Show that the change has happened.
    response = client.call_api(
        'reference_data/maps/rest_api_samples_current_admin_shift', 'GET')
    SampleUtilities.pretty_print_response(response)

    # You can uncomment this line to have this script remove the data it
    # creates after it is done, or you can invoke the Cleanup script directly.
    # Cleanup.cleanup_02_maps(client)


# This helper function sets up data used in this sample.
def setup_data(client):
    SampleUtilities.data_setup(
        client,
        'reference_data/maps?name=rest_api_samples_current_admin_shift&' +
        'element_type=ALN', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/maps/rest_api_samples_current_admin_shift?' +
        'key=7.34.87.23&value=sven', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/maps/rest_api_samples_current_admin_shift?' +
        'key=7.34.85.10&value=sven', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/maps/rest_api_samples_current_admin_shift?' +
        'key=7.34.123.8&value=jill', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/maps/rest_api_samples_current_admin_shift?' +
        'key=7.34.10.5&value=alice', 'POST')


# These functions represent queries made to our HR system to find our which
# administrator is assigned to each server this shift.
def get_second_shift_schedule_from_hr():
    return {'7.34.87.23': 'bob', '7.34.85.10': 'karen', '7.34.123.8': 'karen',
            '7.34.10.5': 'kevin'}


def get_third_shift_schedule_from_hr():
    return {'7.34.87.23': 'joe', '7.34.85.10': 'kim', '7.34.123.8': 'mike'}


# This function updates the reference set with the new shift information.
def update_reference_map(new_shift, current_shift, client):
    # Delete entries from the map if there is no one supervising this server
    # this shift.
    for server_ip in current_shift.keys():
        if (server_ip not in new_shift.keys()):
            client.call_api(
                'reference_data/maps/rest_api_samples_current_admin_shift/' +
                server_ip + '?value=' + current_shift[server_ip]['value'],
                'DELETE')

    # Update the usenames to reflect the administrators on duty this shift.
    for server_ip in new_shift.keys():
        client.call_api(
            'reference_data/maps/rest_api_samples_current_admin_shift?key=' +
            server_ip + '&value=' + new_shift[server_ip], 'POST')


if __name__ == "__main__":
    main()
