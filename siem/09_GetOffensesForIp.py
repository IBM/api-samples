#!/usr/bin/env python3
# This sample demonstrates how to use the siem/source_addresses and
# siem/local_destination_addresses endpoints in the REST API.

# Here we will be showing an example of how to get all offenses associated with
# an IP address. For this scenario to work there must already be offenses on
# the system the sample is being run against.

# The scenario demonstrates the following actions:
#  - Using the GET siem/source_addresses and GET
#    siem/local_destination_addresses endpoints with a filter parameter to get
#    addresses associated with an IP address.
#  - Building a filter criteria to be used with the GET siem/offenses endpoint
#    to get offenses associated with the IP address.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import json
import os
import sys
import ipaddress

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')


def main():
    """
    The entry point for the sample.
    """

    # First we have to create our client.
    api_client = client_module.RestApiClient(version='5.0')

    # Prompt the user for an IP address.
    ip = prompt_for_ip()

    if ip is None:
        sys.exit(1)

    # Get all source addresses associated with the IP address.
    source_addresses = get_source_addresses_for_ip(api_client, ip)

    if source_addresses is None:
        sys.exit(1)

    # Get all local destination addresses associated with the IP address.
    local_destination_addresses = get_local_destination_addresses_for_ip(
        api_client, ip)

    if local_destination_addresses is None:
        sys.exit(1)

    # Combine all offense IDs returned in any of the source or local
    # destination addresses into a single set of unique offense ids.
    offense_ids = set()
    for source_address in source_addresses:
        offense_ids = offense_ids | set(source_address['offense_ids'])
    for local_destination_address in local_destination_addresses:
        offense_ids = (
            offense_ids | set(local_destination_address['offense_ids']))

    # If the set of offense IDs is empty, exit
    if len(offense_ids) == 0:
        print("The set of offense IDs is empty. Cannot continue.")
        sys.exit(1)

    # Generate the filter we will use to return only the offenses associated
    # with the IP address.
    offense_id_filter = generate_filter_from_array('id', offense_ids)

    # Get the offenses associated with the IP address.
    offenses = get_offenses(api_client, offense_id_filter)

    print("The following offenses are associated with the IP address " + ip +
          ":")
    print(json.dumps(offenses, indent=4))


def prompt_for_ip():
    """
    Prompt the user to enter an IP address or "quit" to terminate the sample.
    Any IP address the user enters is validated using the ipaddress module. If
    the user entered an IP address the IP address string is returned, otherwise
    None is returned.
    """

    ip = None
    while ip is None:

        ip = input(
            "Enter an IP address, or quit to terminate the sample: ").strip()

        if ip == "quit":
            return None

        # Use Python's ipaddress module to validate the IP address.
        try:
            parsed_ipaddress = ipaddress.ip_address(ip)
            ip = str(parsed_ipaddress)
        except ValueError as e:
            print(str(e))
            ip = None

    return ip


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


def get_source_addresses_for_ip(api_client, ip):
    """
    Generate a filter for the source_ip field based on the provided ip
    parameter and call the siem/source_addresses with the filter to return
    the addresses associated with the IP address. Returns the list of source
    addresses or None if there was an error.
    """

    endpoint = 'siem/source_addresses'
    params = {'filter': 'source_ip="' + ip + '"'}

    response = api_client.call_api(endpoint, 'GET', params=params,
                                   print_request=True)
    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("Failed to get source addresses.")
        print(response_body)
        return None

    source_addresses = json.loads(response_body)

    return source_addresses


def get_local_destination_addresses_for_ip(api_client, ip):
    """
    Generate a filter for the local_destination_ip field based on the provided
    ip parameter and call the siem/local_destination_addresses with the filter
    to return the addresses associated with the IP address. Returns the list of
    local destination addresses or None if there was an error.
    """

    endpoint = 'siem/local_destination_addresses'
    params = {'filter': 'local_destination_ip="' + ip + '"'}

    response = api_client.call_api(endpoint, 'GET', params=params,
                                   print_request=True)
    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("Failed to get local destination addresses.")
        print(response_body)
        return None

    local_destination_addresses = json.loads(response_body)

    return local_destination_addresses


def get_offenses(api_client, filter):
    """
    Get offense summaries consisting of the following fields from the offense
    structure:

        - id
        - description
        - status
        - offense_type
        - offense_source

    Passes the provided filter parameter to only return only the requested
    offenses. Returns the list of offense summaries or None if there was an
    error.
    """

    endpoint = 'siem/offenses'
    params = {'fields': 'id,description,status,offense_type,offense_source',
              'filter': filter}

    response = api_client.call_api(endpoint, 'GET', params=params,
                                   print_request=True)
    response_body = response.read().decode('utf-8')

    if response.code > 299 or response.code < 200:

        print("API call failed.")
        print(response_body)
        return None

    offenses = json.loads(response_body)

    return offenses

if __name__ == "__main__":
    main()
