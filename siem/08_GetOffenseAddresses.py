#!/usr/bin/env python3
# This sample demonstrates how to use the siem/source_addresses and
# siem/local_destination_addresses endpoints in the REST API.

# Here we will be showing an example of how to get all source addresses and
# local destination addresses for an offense. For this scenario to work there
# must already be offenses on the system the sample is being run against.

# The scenario demonstrates the following actions:
#  - Using GET siem/offenses with filters and fields parameters
#  - Using the output from siem/offenses to build filter criteria to be used
#    with the GET siem/source_addresses and GET
#    siem/local_destination_addresses endpoints.
#  - Using the GET siem/source_addresses and GET
#    siem/local_destination_addresses endpoints with the generated filter
#    criteria to get all source addresses and local destination addresses for
#    an offense.

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


def main():
    """
    The entry point for the sample.
    """

    # First we have to create our client.
    api_client = client_module.RestApiClient(version='5.0')

    # Prompt the user for an offense.
    offense = prompt_for_offense(api_client)

    if offense is None:
        sys.exit(1)

    # Display the offense.
    print("Getting source and local destination addresses for this offense:")
    print(json.dumps(offense, indent=4))

    # Get source addresses associated with the offense and print them to the
    # screen.
    if len(offense['source_address_ids']) > 0:

        print("Getting source addresses.")

        # Generate the filter that returns only the source addresses associated
        # with the offense.
        source_addresses_id_filter = generate_filter_from_array(
            'id', offense['source_address_ids'])

        source_addresses = get_source_addresses(
            api_client, source_addresses_id_filter)

        if source_addresses is not None:
            print("Source addresses associated with the offense:")
            print()
            for source_address in source_addresses:
                print("\t" + source_address['source_ip'])
            print()
    else:
        print("No source addresses on this offense.")

    # Get local destination addresses associated with the offense and print
    # them to the screen.
    if len(offense['local_destination_address_ids']) > 0:

        print("Getting local destination addresses.")

        # Generate the filter that returns only the local destination addresses
        # associated with the offense.
        local_destination_addresses_id_filter = generate_filter_from_array(
            'id', offense['local_destination_address_ids'])

        local_destination_addresses = get_local_destination_addresses(
            api_client, local_destination_addresses_id_filter)

        if local_destination_addresses is not None:
            print("Local destination addresses associated with the offense:")
            print()
            for local_destination_address in local_destination_addresses:
                print("\t" + local_destination_address['local_destination_ip'])
            print()
    else:
        print("No local destination addresses on this offense.")


def prompt_for_offense(api_client):
    """
    Displays summaries of offenses and allows the user to choose an offense by
    entering an offense ID. If the user enters a valid offense ID the offense
    is returned. If the user does not enter a valid ID or if there is an error
    None is returned.
    """

    # Loop until we have a valid offense.
    offense = None
    current_offense = 0
    while offense is None:

        # Get five offense summaries, starting with the current offense.
        offenses = get_offense_summaries(
            api_client, current_offense, current_offense + 4)

        # Return None if there was an error getting the offense summaries.
        if offenses is None:
            return None

        # If zero offenses were returned then we have either already displayed
        # all offenses, or there are no offenses in the system.
        if len(offenses) == 0:

            # If current_offense is 0 then we just tried to get the first five
            # offenses. If no offenses were returned while getting the first
            # five offenses then there are no offenses on the system.
            if current_offense == 0:
                print("No offenses on the system.")
                return None

            # There are offenses on the system, but we have already displayed
            # them all. Reset current_offense to 0 so we can start again from
            # the first offense.
            print("No more offenses on the system. "
                  "Restarting from first offense.")
            current_offense = 0
            continue

        # Display the offense summaries.
        print(json.dumps(offenses, indent=4))

        # Prompt the user for an offense id.
        offense_id = prompt_for_offense_id()

        if offense_id is None:

            # If None is returned if there was an error, or if the user wants
            # to terminate the sample.
            return None

        elif offense_id == "next":

            # If the user entered next then we want to display the next five
            # offenses by incrementing current_offense.
            current_offense = current_offense + 5

        else:

            # The user has entered a valid offense_id, get the offense.
            offense = get_offense(api_client, offense_id)

            # If None was returned then there was a problem getting the
            # offense.
            if offense is None:
                return None

    return offense


def prompt_for_offense_id():
    """
    Prompts the user to enter an offense ID. They could optionally enter "next"
    to indicate they want to see another five offenses, or "quit" to terminate
    the sample. Loops until the user enters valid input.
    """

    # Loop until the user enters valid input.
    offense_id = None
    while offense_id is None:

        offense_id = input(
            "Enter an offense id, next to see another five offenses, or "
            "quit to terminate the sample: ").strip()

        if offense_id == "quit":

            # The user has requested to terminate the sample.
            return None

        # Verify the user has either entered "next" or a valid offense ID.
        offense_id_valid = True
        if offense_id != "next":
            try:
                offense_id_int = int(offense_id)
                if offense_id_int < 0:
                    offense_id_valid = False
            except ValueError:
                offense_id_valid = False

        if not offense_id_valid:

            # If the input was not valid then print a message and continue the
            # loop.
            print(offense_id + " is not valid input.")
            offense_id = None
            continue

    return offense_id


def get_source_addresses(api_client, filter):
    """
    Call the siem/source_addresses endpoint with the provided filter. Returns
    the list of source addresses or None if there was an error.
    """

    endpoint = 'siem/source_addresses'
    params = {'filter': filter}

    response = api_client.call_api(endpoint, 'GET', params=params,
                                   print_request=True)
    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("Failed to get source addresses.")
        print(response_body)
        return None

    source_addresses = json.loads(response_body)

    return source_addresses


def get_local_destination_addresses(api_client, filter):
    """
    Call the siem/local_destination_addresses endpoint with the provided
    filter. Returns the list of local destination addresses or None if there
    was an error.
    """

    endpoint = 'siem/local_destination_addresses'
    params = {'filter': filter}

    response = api_client.call_api(endpoint, 'GET', params=params,
                                   print_request=True)
    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("Failed to get local destination addresses.")
        print(response_body)
        return None

    local_destination_addresses = json.loads(response_body)

    return local_destination_addresses


def get_offense_summaries(api_client, start_offense, end_offense):
    """
    Get offense summaries consisting of the following fields from the offense
    structure:

        - id
        - description
        - status
        - offense_type
        - offense_source
        - source_address_ids
        - local_destination_address_ids

    Passes a Range header with the provided start_offense and end_offense to
    limit the amount of offenses returned. Returns the list of offense
    summaries or None if there was an error.
    """

    endpoint = 'siem/offenses'
    params = {'fields': 'id,description,status,offense_type,offense_source,'
                        'source_address_ids,local_destination_address_ids'}
    headers = {'Range': 'items=' + str(start_offense) + '-' + str(end_offense)}

    response = api_client.call_api(endpoint, 'GET', params=params,
                                   headers=headers, print_request=True)
    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("API call failed.")
        print(response_body)
        return None

    offenses = json.loads(response_body)

    return offenses


def get_offense(api_client, offense_id):
    """
    Get the offense provided with offense_id. Returns the offense or None if
    there was an error.
    """

    endpoint = 'siem/offenses/' + offense_id

    response = api_client.call_api(endpoint, 'GET', print_request=True)
    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("API call failed.")
        print(response_body)
        return None

    offense = json.loads(response_body)

    return offense


def generate_filter_from_array(field_name, array):
    """
    Builds an "in" filter with the provided field_name and values from the
    provided array.
    """

    filter = field_name + " in ("

    first = True
    for item in array:

        if not first:
            filter = filter + ","
        else:
            first = False

        filter = filter + str(item)

    filter = filter + ")"

    return filter

if __name__ == "__main__":
    main()
