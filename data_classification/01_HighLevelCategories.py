#!/usr/bin/env python3
# This sample script demonstrates how to
# 1. get a list of high level categories
# 2. get a single high level category by its id

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
    # 1. get a list of high level categories

    endpoint_url = 'data_classification/high_level_categories'
    http_method = 'GET'

    # 'fields' is used to limit the fields returned for each record
    fields = 'id, name'

    # 'query_filter' is used to filter the list returned based on field values
    query_filter = 'name ilike "risk"'

    # 'sort' is used to sort list based on applicable fields
    sort = '+name'

    # populate the optional parameters to be used in request
    params = {'fields': fields, 'filter': query_filter, 'sort': sort}

    # send the request
    response = client.call_api(endpoint_url, http_method, params=params,
                               print_request=True)

    # check response and handle any error
    if response.code == 200:
        # extract records from response
        high_level_categories = json.loads(response.read().decode('utf-8'))
        print(high_level_categories)
    else:
        print('Failed to get the list of high level categories')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 2. get a single high level category by its id

    high_level_category_id = 3000

    endpoint_url = ('data_classification/high_level_categories' + '/' +
                    str(high_level_category_id))

    # send the request
    response = client.call_api(endpoint_url, http_method, print_request=True)

    # check response and handle any error
    if response.code == 200:
        # extract record from response
        high_level_category = json.loads(response.read().decode('utf-8'))
        print(high_level_category)
    else:
        print('Failed to get the high level category with id=' +
              str(high_level_category_id))
        SampleUtilities.pretty_print_response(response)


if __name__ == "__main__":
    main()
