#!/usr/bin/env python3
# This sample demonstrates how to use the
# /qvm/saved_searches/vuln_instances/{task_id}/results/vuln_instances
# endpoint in the REST API.
from re import search

# - For this scenario to work there must already be vulnerability instances on
# -   the system the sample is being run against.

# - The scenario demonstrates the following actions:
#    - How to get specific QVM saved search.
#    - How to use QVM saved search to create vulnerability instances search.
#    - How to check current status of a vulnerability instance search.
#    - How to get vulnerability instances returned from a QVM saved search
#    - How to get assets returned from a QVM saved search
#    - How to get vulnerabilities returned from a QVM saved search
#    - How to use 'Range' header for pagination

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/endpoints endpoint.

import sys
import os
import json
import time

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Constants
    TASK_CHECK_PROGRESS_WAIT_TIME = 5  # secs
    TASK_TIMEOUT = 18000  # secs

    # Create our client.
    client = client_module.RestApiClient(version='6.0')

    # Using the /qvm/saved_searches endpoint with a GET request to get 'High
    # risk' saved search
    saved_searches_endpoint_url = 'qvm/saved_searches?' \
        'filter=name="High%20risk"'
    SampleUtilities.pretty_print_request(client, saved_searches_endpoint_url,
                                         'GET')
    # URL Encoding
    # - convert a space into %20
    response = client.call_api(saved_searches_endpoint_url, 'GET')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print('Failed to retrieve saved search list.')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # The number of saved searches retrieved.
    response_body = json.loads(response.read().decode('utf-8'))
    number_of_searches_retrieved = len(response_body)

    # Display number of searches, and the names of the searches retrieved.
    print(str(number_of_searches_retrieved) +
          ' saved searches were retrieved.\n')
    print('Available QVM Saved Searches:')
    print(json.dumps(response_body, indent=2))

    # Retrieve the saved search unique identifier
    saved_search_id = str(response_body[0]['id'])
    saved_search_name = str(response_body[0]['name'])

    print('Running saved search : ' + saved_search_name)

    # Create a vulnerability instances search by using saved search id
    # Using the /asset_model/saved_searches/{saved_search_id}/vuln_instances
    # endpoint with a GET request.
    # The search is asynchronous, so the response will not be the results of
    # the search.
    search_endpoint_url = ('qvm/saved_searches/' +
                           saved_search_id + '/vuln_instances')
    SampleUtilities.pretty_print_request(client, search_endpoint_url,
                                         'GET')
    response = client.call_api(search_endpoint_url, 'GET')
    response_body = json.loads(response.read().decode('utf-8'))

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    if(response.code != 201):
        print(
            "Failed to create vulnerability instance search " +
            "with saved search id " + saved_search_id)
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # get the task id
    task_id = str(response_body['id'])
    # get retention_period_in_days
    retention_period_in_days = str(response_body['retention_period_in_days'])
    # task status
    status = str(response_body['status'])

    # Print response
    print('Task Id: ' + task_id)
    print('Retention period in days: ' + retention_period_in_days)
    print('Task Status: ' + status + '\n')

    # Check task status
    task_status_endpoint_url = ('qvm/saved_searches/vuln_instances/' +
                                task_id + '/status')
    SampleUtilities.pretty_print_request(client, task_status_endpoint_url,
                                         'GET')
    response = client.call_api(task_status_endpoint_url, 'GET')
    status = str(response_body['status'])
    print('Task Status: ' + status + '\n')

    # Verify that the call to the API was successful.
    if (response.code != 200):
        print(
            'Failed to retrieve status of a vulnerability instance search ' +
            'using task id: ' + task_id)
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # This block of code calls GET
    # /qvm/saved_searches/vuln_instances/{task_id}/status
    # on the QVM API to determine if the task is complete.
    # This block of code will repeat until the status of
    # the search is 'COMPLETE' or there is an error.
    response_body = json.loads(response.read().decode('utf-8'))
    task_progress_time = 0  # secs
    error = False
    while (response_body['status'] != 'COMPLETED') and not error:
        if (response_body['status'] == 'QUEUED') | \
                (response_body['status'] == 'PROCESSING'):
            # Check task status
            SampleUtilities.pretty_print_request(client,
                                                 task_status_endpoint_url,
                                                 'GET')
            response = client.call_api(task_status_endpoint_url, 'GET')

            # Verify that the call to the API was successful.
            if (response.code != 200):
                print(
                    'Failed to retrieve status of a vulnerability instance ' +
                    'search using task id: ' + task_id)
                SampleUtilities.pretty_print_response(response)
                sys.exit(1)

            response_body = json.loads(response.read().decode('utf-8'))
            status = str(response_body['status'])
            print('Task Status: ' + status + '\n')

            # Wait for 5 seconds before the call to the get task status API
            time.sleep(TASK_CHECK_PROGRESS_WAIT_TIME)
            task_progress_time = task_progress_time + \
                TASK_CHECK_PROGRESS_WAIT_TIME

            # If the search is queued or taking too long to process then we
            # should exit
            if (task_progress_time == TASK_TIMEOUT):
                print(
                    'Failed to run vulnerability instance search using ' +
                    'task id: %s due to timeout at %s secs.  Task status is %s'
                    % (task_id, TASK_TIMEOUT, response_body['status']))
                sys.exit(1)

        else:
            print(response_body['status'])
            error = True

    if (error):
        print(
            'Failed to retrieve current status of a vulnerability instance ' +
            'search using task id: ' + task_id)
        sys.exit(1)

    # After the search is complete, call the
    # GET /qvm/saved_searches/vuln_instances/{task_id}/results/vuln_instances
    # to obtain Vulnerability Instances returned from the search.
    vuln_instances_results_endpoint_url = (
        'qvm/saved_searches/vuln_instances/' + task_id +
        '/results/vuln_instances')
    # If this set contained a large amount of data, we might want to process it
    # a little bit at a time. We are going to use pagination to get 10 rows of
    # vulnerability instances results at a time until we get a total of 30 rows
    # back.
    # To get back only part of the data we can use a 'Range' header.
    # Note that the range header is indexed form zero, so here we are asking
    # for the first 10 items.
    for i in range(0, 3):

        print(
            '===============================================================' +
            '========================================\n')
        print(
            'Page %s.  Trying to get back 10 rows of ' % str(i + 1) +
            'vulnerability instances')
        range_header = {
            'Range': 'items=' + str(i * 10) + '-' + str((i * 10) + 9)}
        SampleUtilities.pretty_print_request(
            client, vuln_instances_results_endpoint_url, 'GET',
            headers=range_header)
        response = client.call_api(vuln_instances_results_endpoint_url,
                                   'GET', headers=range_header)

        # Verify that the call to the API was successful.
        if (response.code != 200):
            print(
                'Failed to retrieve vulnerability instances results using ' +
                'task id: ' + task_id)
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)

        response_body = json.loads(response.read().decode('utf-8'))

        # Get the number of saved searches retrieved.
        number_of_vuln_instances_retrieved = len(response_body)

        # If we have vulnerability instances then get more info
        if (number_of_vuln_instances_retrieved > 0):

            # Display the number of vulnerability instances retrieved and
            # vulnerability instances JSON object
            print(str(number_of_vuln_instances_retrieved) +
                  ' vulnerability instances were retrieved.\n')
            print('Available vulnerability Instances:')
            print(json.dumps(response_body, indent=2))

            # Build a set of associated asset ids and vulnerability ids
            # (use sets because we don't care about duplicates)
            # so that we can use it to call other APIs to get more info
            asset_id_set = set()
            vuln_id_set = set()
            for vuln_instances in response_body:
                asset_id_set.add(str(vuln_instances['asset_id']))
                vuln_id_set.add(str(vuln_instances['vulnerability_id']))

            # convert list of ids into a comma separated list of string
            asset_id_str_list = ",".join(str(x) for x in asset_id_set)
            vuln_id_str_list = ",".join(str(x) for x in vuln_id_set)

            print('\nSet of asset ids: ' + asset_id_str_list)
            print('Set of vulnerability ids: ' + vuln_id_str_list + '\n')

            # get the number of assets
            num_of_assets = len(asset_id_set)
            print('Getting ' + str(num_of_assets) + ' rows of assets\n')

            # If we have assets then get more asset info
            if (num_of_assets > 0):
                # Get asset info by using a list of asset ids and
                # using the
                # /qvm/saved_searches/vuln_instances/{task_id}/results/assets
                # endpoint with a GET request.
                #     URL Encoding
                #         - convert a space into %20
                assets_results_endpoint_url = (
                    'qvm/saved_searches/vuln_instances/' +
                    task_id + '/results/assets?filter=id%20IN%20(' +
                    asset_id_str_list + ')')
                SampleUtilities.pretty_print_request(
                    client, assets_results_endpoint_url, 'GET')
                response = client.call_api(assets_results_endpoint_url,
                                           'GET')

                # Verify that the call to the API was successful.
                if (response.code != 200):
                    print(
                        'Failed to retrieve vulnerability instances results ' +
                        'using task id: ' + task_id)
                    SampleUtilities.pretty_print_response(response)
                    sys.exit(1)

                response_body = json.loads(response.read().decode('utf-8'))

                # Get the number of assets retrieved.
                number_of_assets_retrieved = len(response_body)

                # Display the number of assets retrieved and asset JSON objects
                print(str(number_of_assets_retrieved) +
                      ' assets were retrieved.\n')
                print('Available Assets:')
                print(json.dumps(response_body, indent=2))
                print('\n')

            # get the number of vulnerabilities
            num_of_vulns = len(vuln_id_set)
            print(
                'Getting ' + str(num_of_vulns) + ' rows of vulnerabilities\n')

            # If we have vulnerabilities then get more vulnerability info
            if (num_of_vulns > 0):
                # Get vulnerability info by using a list of vulnerability ids
                # and using the
                # /qvm/saved_searches/vuln_instances/{task_id}/results/vulnerabilities
                # endpoint with a GET request.
                #     URL Encoding
                #         - convert a space into %20
                vulnerabilities_results_endpoint_url = (
                    'qvm/saved_searches/vuln_instances/' +
                    task_id + '/results/vulnerabilities?filter=id%20IN%20(' +
                    vuln_id_str_list + ')')
                SampleUtilities.pretty_print_request(
                    client, vulnerabilities_results_endpoint_url, 'GET')
                response = client.call_api(
                    vulnerabilities_results_endpoint_url, 'GET')

                # Verify that the call to the API was successful.
                if (response.code != 200):
                    print(
                        'Failed to retrieve vulnerabilities results using ' +
                        'task id: ' + task_id)
                    SampleUtilities.pretty_print_response(response)
                    sys.exit(1)

                response_body = json.loads(response.read().decode('utf-8'))

                # Get the number of vulnerabilities retrieved.
                number_of_vulnerabilities_retrieved = len(response_body)

                # Display the number of vulnerabilities retrieved and asset
                # JSON objects
                print(str(number_of_vulnerabilities_retrieved) +
                      ' vulnerabilities were retrieved.\n')
                print('Available Vulnerabilities:')
                print(json.dumps(response_body, indent=2))

if __name__ == "__main__":
    main()
