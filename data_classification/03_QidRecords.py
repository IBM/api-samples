#!/usr/bin/env python3
# This sample demonstrates how to
#  1. get a list of qid records
#  2. create a new qid record
#  3. get a single qid record by its id
#  4. update fields of an existing qid record

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
    # 1. get a list of qid records

    endpoint_url = 'data_classification/qid_records'
    http_method = 'GET'

    # select fields to return for each qid record
    fields = 'qid, name'

    # use filter to select desired qid record
    query_filter = 'name ilike "%authentication%" '

    # populate the optional parameters to be used in request
    params = {'fields': fields, 'filter': query_filter}

    # put range in header for paging purpose
    headers = {'range': 'items=0-5'}

    # send the request
    response = client.call_api(endpoint_url, http_method, params=params,
                               headers=headers, print_request=True)

    # handle response
    if response.code == 200:
        qid_records = json.loads(response.read().decode('utf-8'))
        # go through the returned list of qid records and print each one
        for qid_record in qid_records:
            print(qid_record)

    else:
        print('Failed to retrieve the list of qid records')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 2. create a new qid record
    endpoint_url = 'data_classification/qid_records'
    http_method = 'POST'

    new_qid_record = {'log_source_type_id': 2,
                      'name': 'qid record created from api sample',
                      'severity': 5,
                      'low_level_category_id': 1008
                      }

    data = json.dumps(new_qid_record).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 201:
        print('A new qid record is created.')
        # can extract qid record from the response for further manipulation
        qid_record = json.loads(response.read().decode('utf-8'))
        print(json.dumps(qid_record, indent=4))
    else:
        print('Failed to create the new qid record')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 3. get a single qid record by its id

    # using qid record created in step 2
    qid_record_id = qid_record['id']

    endpoint_url = ('data_classification/qid_records' + '/' +
                    str(qid_record_id))
    http_method = 'GET'

    # send the request
    response = client.call_api(endpoint_url, http_method, print_request=True)

    # check response and handle any error
    if response.code == 200:
        qid_record = json.loads(response.read().decode('utf-8'))
        print(json.dumps(qid_record, indent=4))
    else:
        print('Failed to retrieve the qid record with id=' +
              str(qid_record_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 4. update a qid record by id

    # using qid record created in step 2
    qid_record_id = qid_record['id']

    endpoint_url = ('data_classification/qid_records' + '/' +
                    str(qid_record_id))
    http_method = 'POST'

    fields_to_update = {'name': 'an updated qid record name',
                        'severity': 8
                        }

    data = json.dumps(fields_to_update).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 200:
        udpated_qid_record = json.loads(response.read().decode('utf-8'))
        print(json.dumps(udpated_qid_record, indent=4))
    else:
        print('Failed to update the qid record with id=' +
              str(qid_record_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

if __name__ == "__main__":
    main()
