#!/usr/bin/env python3
# This sample script demonstrates how to
# 1. get a list of low level categories
# 2. get a single low level category by its id

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
    # 1. get a list of low level categories

    endpoint_url = 'data_classification/low_level_categories'
    http_method = 'GET'

    # 'fields' is used to limit the fields returned for each record
    fields = 'id, name'

    # 'query_filter' is used to filter the list returned based on field values
    # low_level_category_id can be used in the filter to get a list of low
    # level categories belonging to the specified high level category
    query_filter = 'high_level_category_id = 4000'

    # 'sort' is used to sort list based on applicable fields
    sort = '+id'

    # populate the optional parameters to be used in request
    params = {'fields': fields, 'filter': query_filter, 'sort': sort}

    # send the request
    response = client.call_api(endpoint_url, http_method, params=params,
                               print_request=True)

    # check response and handle any error
    if response.code == 200:
        # extract records from response
        low_level_categories = json.loads(response.read().decode('utf-8'))
        print(low_level_categories)
    else:
        print('Failed to get the list of low level categories')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 2. get a single low level category by its id

    low_level_category_id = 3001

    endpoint_url = ('data_classification/low_level_categories' + '/' +
                    str(low_level_category_id))

    # send the request
    response = client.call_api(endpoint_url, http_method, print_request=True)

    # check response and handle any error
    if response.code == 200:
        # extract record from response
        low_level_category = json.loads(response.read().decode('utf-8'))
        print(low_level_category)
    else:
        print('Failed to get the low level category with id=' +
              str(low_level_category_id))
        SampleUtilities.pretty_print_response(response)

if __name__ == "__main__":
    main()
