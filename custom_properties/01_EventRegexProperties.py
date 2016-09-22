#!/usr/bin/env python3
# This sample script demonstrates how to
# 1. get a list of event regex properties
# 2. create a new event regex property
# 3. get an event regex property by id
# 4. update an existing event regex property
# 5. start a find dependents task and check results when completed
# 6. start a deletion task to remove an existing event regex property

import importlib
import json
import os
import sys

from taskManager import TaskManager


sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # create the api client
    client = client_module.RestApiClient(version='7.0')

    # -------------------------------------------------------------------------
    # 1. get a list of event regex property
    endpoint_url = 'config/event_sources/custom_properties/regex_properties'
    http_method = 'GET'

    # select fields to return for each event regex property
    fields = 'id, name, property_type'

    # use filter to select desired event regex property
    query_filter = 'property_type = "numeric"'

    # populate the optional parameters to be used in request
    params = {'fields': fields, 'filter': query_filter}

    # put range in header for paging purpose
    headers = {'range': 'items=0-4'}

    # send the request
    response = client.call_api(endpoint_url, http_method, params=params,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 200:
        regex_properties = json.loads(response.read().decode('utf-8'))

        # go through the list of event regex properties and print each
        for regex_property in regex_properties:
            print(regex_property)

    else:
        SampleUtilities.pretty_print_response(response)
        print('Failed to retrieve the list of event regex properties')
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 2. create a new event regex property

    endpoint_url = 'config/event_sources/custom_properties/regex_properties'
    http_method = 'POST'

    # sample event regex property, be sure to change the name if running
    # multiple times.
    new_regex_property = {
                                "name": "Sample event regex property x",
                                "description": "description property",
                                "property_type": "numeric",
                                "use_for_rule_engine": True,
                                }

    data = json.dumps(new_regex_property).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 201:
        print('A new event regex property is created.')
        # can extract newly created event regex property from the response
        regex_property = json.loads(response.read().decode('utf-8'))
        print(json.dumps(regex_property, indent=4))
    else:
        print('Failed to create the new event regex property')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 3. get a single event regex property by id

    # id of the event regex property, using the one created in step 2
    regex_property_id = regex_property['id']

    endpoint_url = ('config/event_sources/custom_properties/regex_properties' +
                    '/' + str(regex_property_id))
    http_method = 'GET'

    # send the request
    response = client.call_api(endpoint_url, http_method, print_request=True)

    # check response and handle any error
    if response.code == 200:
        print("The requested event regex property has been retrieved.")
        regex_property = json.loads(response.read().decode('utf-8'))
        print(json.dumps(regex_property, indent=4))
    else:
        print('Failed to retrieve the event regex property with id=' +
              str(regex_property_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 4. update an event regex property by its id

    # using event regex property created in step 2
    regex_property_id = regex_property['id']

    endpoint_url = ('config/event_sources/custom_properties/regex_properties' +
                    '/' + str(regex_property_id))
    http_method = 'POST'

    fields_to_update = {
                        'description': 'updated description',
                        'use_for_rule_engine': False,
                        }

    data = json.dumps(fields_to_update).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    if response.code == 200:
        print('The event regex property has been successfully updated.')
        regex_property = json.loads(response.read().decode('utf-8'))
        print(json.dumps(regex_property, indent=4))
    else:
        print('Failed to update the event regex property with id=' +
              str(regex_property_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 5. find dependents of an event regex property

    # using event regex property created in step 2
    regex_property_id = regex_property['id']

    endpoint_url = ('config/event_sources/custom_properties/regex_properties' +
                    '/' + str(regex_property_id)) + '/dependents'
    http_method = 'GET'

    # send the request
    response = client.call_api(endpoint_url, http_method, print_request=True)

    if response.code == 202:
        print('The find dependents task for event regex property has started.')
        task_status = json.loads(response.read().decode('utf-8'))
        print(json.dumps(task_status, indent=4))

        task_status_url = ('/config/event_sources/custom_properties/' +
                           'regex_property_dependent_tasks' + '/' +
                           str(task_status['id']))

        task_manager = TaskManager(client, task_status_url)

        try:
            task_manager.wait_for_task_to_complete(60)

            # query the result endpoint for results

            endpoint_url = ('config/event_sources/custom_properties/' +
                            'regex_property_dependent_tasks' + '/' +
                            str(task_status['id']) + '/results')
            http_method = 'GET'

            response = client.call_api(endpoint_url, http_method,
                                       print_request=True)

            # check response and handle any error
            if response.code == 200:
                task_result = json.loads(response.read().decode('utf-8'))
                print(json.dumps(task_result, indent=4))

            else:
                SampleUtilities.pretty_print_response(response)
                print('Failed to retrieve the result of find dependents task.')
                sys.exit(1)

        except TimeoutError:
            print("Find dependents task time out. Current status is:")
            SampleUtilities.pretty_print_response(
                              task_manager.get_task_status()
                              )

    else:
        print('Failed to start a find dependents task for ' +
              'event regex property with id=' + str(regex_property_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 6. delete an event regex property

    # using event regex property created in step 2
    regex_property_id = regex_property['id']

    endpoint_url = ('config/event_sources/custom_properties/regex_properties' +
                    '/' + str(regex_property_id))
    http_method = 'DELETE'

    # send the request
    response = client.call_api(endpoint_url, http_method, print_request=True)

    if response.code == 202:
        print('The deletion task for event regex property has started.')
        task_status = json.loads(response.read().decode('utf-8'))
        print(json.dumps(task_status, indent=4))

        task_status_url = ('/config/event_sources/custom_properties/' +
                           'regex_property_delete_tasks' + '/' +
                           str(task_status['id']))

        task_manager = TaskManager(client, task_status_url)

        try:
            task_manager.wait_for_task_to_complete(60)
        except TimeoutError:
            print("Deletion task time out. Current status is:")
            SampleUtilities.pretty_print_response(
                              task_manager.get_task_status()
                              )

    else:
        print('Failed to start a deletion task for ' +
              'event regex property with id=' + str(regex_property_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

if __name__ == "__main__":
    main()
