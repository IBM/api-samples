#!/usr/bin/env python3
# In this sample you will see how to limit the data returned by an endpoint
# using some shared parameters. The 'filter' query parameter can be used to
# restrict the elements returned in a list based on the contents of the fields
# being returned. The 'Range' header parameter can be used to page the elements
# of a list by specifying the start and end values of the range you want. the
# 'fields' query parameter is used to specify the fields in the return object
# you are interested in. Only those fields will be returned in the response.
# This sample uses the reference_data/sets endpoints as an example, but these
# parameters can be applied to many other endpoints.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.

import json
import os
import sys
import time

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Create our client and set up some sample data.
    client = client_module.RestApiClient(version='5.0')
    setup_data(client)

    # First lets have a look at the data in this reference set
    SampleUtilities.pretty_print_request(client, 'reference_data/sets', 'GET')
    response = client.call_api('reference_data/sets', 'GET')
    SampleUtilities.pretty_print_response(response)

    # Suppose we are only interested in the names and the size of each set. We
    # can restrict the data we get back with a 'fields' parameter.
    params = {'fields': 'name,number_of_elements'}
    response = client.call_api('reference_data/sets', 'GET', params=params,
                               print_request=True)
    SampleUtilities.pretty_print_response(response)

    # If this set contained a large amount of data, we might want to process it
    # a little bit at a time. To get back only part of the data we can use a
    # 'Range' header.
    # Note that the range header is indexed form zero, so here we are asking
    # for the first 5 items.
    range_header = {'Range': 'items=0-4'}
    SampleUtilities.pretty_print_request(client, 'reference_data/sets', 'GET',
                                         headers=range_header)
    response = client.call_api('reference_data/sets', 'GET',
                               headers=range_header)
    response_headers = response.info()
    SampleUtilities.pretty_print_response(response)

    # Note that there is a header in the response that contains information
    # about the portion of the data that you requested.
    # the 'Content-Range' header tells you which items you got back and how
    # many items are in the whole list.
    print('Content-Range header value: ' + response_headers['Content-Range'])

    parsed_range_header = response_headers['Content-Range'].split('/')

    print('This tells us which items we got back: ' + parsed_range_header[0])
    print('This tells us how many items there are in total: ' +
          parsed_range_header[1])

    # We can use this information to get back the data one page at a time
    current_position = 5
    while(current_position < int(parsed_range_header[1])):
        range_string = ('items=' + str(current_position) + '-' +
                        str(current_position + 4))
        range_header = {'Range': range_string}
        SampleUtilities.pretty_print_request(client, 'reference_data/sets',
                                             'GET', headers=range_header)
        response = client.call_api('reference_data/sets', 'GET',
                                   headers=range_header)
        print((response.info())['Content-Range'])
        SampleUtilities.pretty_print_response(response)
        current_position = current_position + 5

    # Now suppose that we want to find a specific set that contains data we are
    # interested in. We can use the filter parameter to do this.
    # Some sets were added during the setup of this sample script. Lets find
    # them.
    params = {'filter': 'name between rest_api_samples and rest_api_samplet'}
    response = client.call_api('reference_data/sets', 'GET', params=params,
                               print_request=True)
    SampleUtilities.pretty_print_response(response)

    # Only some of these sets contain data.
    params = {'filter': 'name between rest_api_samples and rest_api_samplet '
                        'and number_of_elements > 0'}
    response = client.call_api('reference_data/sets', 'GET', params=params,
                               print_request=True)
    SampleUtilities.pretty_print_response(response)

    response = client.call_api('reference_data/sets', 'GET', params=params,
                               print_request=True)
    parsed_response = json.loads(response.read().decode('utf-8'))

    for ref_data_set in parsed_response:
        print('The sample reference set ' + ref_data_set['name'] +
              ' contains data')

    # the filter parameter supports:
    # and, or, and not logical operators as well as brackets to specify
    # precedence.
    # =, >, <, >=, <=, !=, in, between, is null comparisons.
    # Refer to your product documentation for more information about using
    # filters.

    # You can combine fields, filters, and the range parameter to have precise
    # control over the data you get back from the API.
    # Here we are asking for only the names of the top two reference sets that
    # were added by this sample script.
    params = {'filter': 'name between rest_api_samples and rest_api_samplet',
              'fields': 'name'}
    headers = {'Range': 'items=0-1'}
    response = client.call_api('reference_data/sets', 'GET', params=params,
                               headers=headers, print_request=True)
    SampleUtilities.pretty_print_response(response)

    # You can uncomment this line to have this script remove the data it
    # creates after it is done, or you can invoke the Cleanup script directly.
    # Cleanup.cleanup_06_filtering(client)


# This helper function sets up data used in this sample.
def setup_data(client):
    SampleUtilities.data_setup(
        client,
        'reference_data/sets?name=rest_api_samples_authorized_users&' +
        'element_type=ALN', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets/rest_api_samples_authorized_users?value=dave',
        'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets?name=rest_api_samples_authorized_ips&' +
        'element_type=IP', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets?name=rest_api_samples_keywords&' +
        'element_type=ALNIC', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets/rest_api_samples_keywords?value=sample', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets?name=rest_api_samples_authorized_ports&' +
        'element_type=PORT', 'POST')
    SampleUtilities.data_setup(
        client,
        'reference_data/sets?name=rest_api_samples_recent_access&' +
        'element_type=DATE', 'POST')

if __name__ == "__main__":
    main()
