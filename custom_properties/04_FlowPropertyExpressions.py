#!/usr/bin/env python3
# This sample script demonstrates how to
# 1. get a list of flow property expressions
# 2. create a new flow property expression
# 3. get a flow property expression by id
# 4. update an existing flow property expression
# 5. delete a flow property expression

import importlib
import json
import os
import sys

sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # create the api client
    client = client_module.RestApiClient(version='7.0')

    # -------------------------------------------------------------------------
    # 1. get a list of flow property expressions

    endpoint_url = ('config/flow_sources/custom_properties/' +
                    'property_expressions')
    http_method = 'GET'

    # select fields to return for each flow property expression
    fields = 'id, regex, qid, payload_origin'

    # use filter to select desired flow property expression
    query_filter = 'regex ilike "%http%"'

    # populate the optional parameters to be used in request
    params = {'fields': fields, 'filter': query_filter}

    # put range in header for paging purpose
    headers = {'range': 'items=0-5'}

    # send the request
    response = client.call_api(endpoint_url, http_method, params=params,
                               headers=headers, print_request=True)

    # handle response
    if response.code == 200:
        expressions = json.loads(response.read().decode('utf-8'))
        # go through the returned list of expressions and print each one
        for expression in expressions:
            print(expression)

    else:
        print('Failed to retrieve the list of expressions')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 2. create a new flow property expression

    # create a new regex property to link to the expression
    # be sure to change the name if running this multiple times
    new_regex_property = {
                          "name": "regex property for the new expression y",
                          "property_type": "numeric",
                          "use_for_rule_engine": True,
                          }

    regex_property = create_sample_regex_property(
                                                  client,
                                                  new_regex_property
                                                  )

    new_property_expression = {
            "regex_property_identifier": regex_property['identifier'],
            "capture_group": 1,
            "enabled": True,
            "payload_origin": "source_payload",
            "qid": 38750003,
            "regex": "session duration = (\\d+) hours, (\\d+) minutes",
            }

    endpoint_url = ('config/flow_sources/' +
                    'custom_properties/property_expressions')
    http_method = 'POST'

    data = json.dumps(new_property_expression).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 201:
        print('A new expression is created.')
        # can extract expression from the response for further manipulation
        expression = json.loads(response.read().decode('utf-8'))
        print(json.dumps(expression, indent=4))
    else:
        print('Failed to create the new expression')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 3. get a single expression by its id

    # using expression created in step 2
    expression_id = expression['id']

    endpoint_url = (
            'config/flow_sources/custom_properties/property_expressions' +
            '/' + str(expression_id))
    http_method = 'GET'

    # send the request
    response = client.call_api(endpoint_url, http_method, print_request=True)

    # check response and handle any error
    if response.code == 200:
        property_expression = json.loads(response.read().decode('utf-8'))
        print(json.dumps(property_expression, indent=4))
    else:
        print('Failed to retrieve the expression with id=' +
              str(expression_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 4. update an expression by id

    # using expression created in step 2
    expression_id = property_expression['id']

    endpoint_url = (
            'config/flow_sources/custom_properties/property_expressions' +
            '/' + str(expression_id))
    http_method = 'POST'

    fields_to_update = {
                        "regex": "session duration = (\\d+) hours",
                        }

    data = json.dumps(fields_to_update).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 200:
        updated_expression = json.loads(response.read().decode('utf-8'))
        print(json.dumps(updated_expression, indent=4))
    else:
        print('Failed to update the expression with id=' +
              str(expression_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 5. delete a flow property expression

    # using flow property expression created in step 2
    expression_id = property_expression['id']

    endpoint_url = (
            'config/flow_sources/custom_properties/property_expressions' +
            '/' + str(expression_id))
    http_method = 'DELETE'

    headers = {'Accept': 'text/plain'}

    # send the request
    response = client.call_api(endpoint_url, http_method,
                               headers=headers, print_request=True)

    if response.code == 204:
        print('The flow property expression has been deleted.')

    else:
        print('Failed to delete the flow property expression with id = ' +
              str(expression_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)


def create_sample_regex_property(client, new_regex_property):

    endpoint_url = 'config/flow_sources/custom_properties/regex_properties'
    http_method = 'POST'

    data = json.dumps(new_regex_property).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 201:
        print('A new regex property is created.')
        # can extract newly created regex property from the response
        regex_property = json.loads(response.read().decode('utf-8'))
        print(json.dumps(regex_property, indent=4))
        return regex_property
    else:
        print('Failed to create the new regex property')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)


if __name__ == "__main__":
    main()
