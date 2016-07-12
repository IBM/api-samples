#!/usr/bin/env python3
# In this sample you will see how data in reference sets can be manipulated
# using the REST API.

# In this scenario we have already configured two reference sets in the
# product,one to capture ip addresses exhibiting suspect behavior and another
# to hold blocked ip addresses.

# A custom rule is defined to identify suspect ip addresses based on business
# rules.
# A second rule is defined to generate offenses based on blocked ip addresses
# accessing certain network resources.

# Our company has a legacy system that contains data and software that can
# choose ip addresses to block based on custom criteria and upload these IP
# addresses to our company's firewalls. We would like to integrate this logic
# with the data in our reference set so that suspected ip addresses collected
# by the product can be validated by this system and so that ip addresses
# blocked by this system can be monitored by the product to ensure they are
# properly excluded from our network.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/endpoints endpoint.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Create our client and set up some sample data.
    client = client_module.RestApiClient(version='6.0')
    setup_data(client)

    # Using the '/sets/{name} endpoint with a GET request we can retrieve the
    # contents of our set of suspect addresses.
    SampleUtilities.pretty_print_request(
        client, 'reference_data/sets/rest_api_samples_suspect_ips', 'GET')
    response = client.call_api(
        'reference_data/sets/rest_api_samples_suspect_ips', 'GET')

    # Based on our business rules, this set should always exist. If it does not
    # exist it could be an indication that our security has been breached and
    # that an attack is in progress. We should raise an alarm.
    if (response.code == 404):
        print('Something is wrong, a system administrator should investigate.')
        sys.exit(1)

    # Extract the reference set from the response body.
    response_body = json.loads(response.read().decode('utf-8'))
    data = response_body['data']

    for element in data:

        # For each suspect ip address, pass it to our legacy system to
        # validate. If it is a real threat, move it to the blocked list so that
        # the configured rules can generate offenses if it is active on our
        # network.
        ip_address = element['value']
        if (legacy_system_logic(ip_address)):
            SampleUtilities.pretty_print_request(
                client,
                'reference_data/sets/rest_api_samples_blocked_ips?value=' +
                ip_address, 'POST')
            response = client.call_api(
                'reference_data/sets/rest_api_samples_blocked_ips?value=' +
                ip_address, 'POST')

            SampleUtilities.pretty_print_request(
                client, 'reference_data/sets/rest_api_samples_suspect_ips/' +
                ip_address, 'DELETE')
            response = client.call_api(
                'reference_data/sets/rest_api_samples_suspect_ips/' +
                ip_address, 'DELETE')

    # The result of this processing is that there are some ip addresses now in
    # the blocked list.
    response = client.call_api(
        'reference_data/sets/rest_api_samples_suspect_ips', 'GET')
    SampleUtilities.pretty_print_response(response)

    # The ip addresses that were not blocked are sill in the suspect list for
    # us to watch.
    response = client.call_api(
        'reference_data/sets/rest_api_samples_blocked_ips', 'GET')
    SampleUtilities.pretty_print_response(response)

    # You can uncomment this line to have this script remove the data it
    # creates after it is done, or you can invoke the Cleanup script directly.
    # Cleanup.cleanup_01_sets(client)


# This helper function sets up data used in this sample.
def setup_data(client):
    SampleUtilities.data_setup(
        client,
        'reference_data/sets?name=rest_api_samples_suspect_ips&' +
        'element_type=IP', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets/rest_api_samples_suspect_ips?value=8.7.6.5',
        'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets/rest_api_samples_suspect_ips?value=10.7.6.5',
        'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets/rest_api_samples_suspect_ips?value=13.7.6.5',
        'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets?name=rest_api_samples_blocked_ips&' +
        'element_type=IP', 'POST')


# This function represents logic performed by a legacy system.
def legacy_system_logic(ip_address):
    if (ip_address[0] == '1'):
        return True
    else:
        return False


if __name__ == "__main__":
    main()
