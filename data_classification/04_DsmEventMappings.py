#!/usr/bin/env python3
# This sample demonstrates how to
#  1. get a list of dsm event mappings
#  2. create a new dsm event mapping
#  3. get a single dsm event mapping by its id
#  4. update fields of an existing dsm event mapping

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
    # 1. get a list of dsm event mapping
    endpoint_url = 'data_classification/dsm_event_mappings'
    http_method = 'GET'

    # select fields to return for each dsm event mapping
    fields = ('log_source_type_id, log_source_event_category,' +
              'log_source_event_id, custom_event, qid_record_id')

    # use filter to select desired dsm event mapping
    query_filter = 'log_source_type_id = 2'

    # populate the optional parameters to be used in request
    params = {'fields': fields, 'filter': query_filter}

    # put range in header for paging purpose
    headers = {'range': 'items=0-4'}

    # send the request
    response = client.call_api(endpoint_url, http_method, params=params,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 200:
        dsm_event_mappings = json.loads(response.read().decode('utf-8'))

        # go through the returned list of dsm event mappings and print each one
        for dsm_event_mapping in dsm_event_mappings:
            print(dsm_event_mapping)

    else:
        SampleUtilities.pretty_print_response(response)
        print('Failed to retrieve the list of dsm event mappings')
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 2. create a new dsm event mapping

    # create a new qid record first to be mapped to the dsm event
    new_qid_record = {'log_source_type_id': 2,
                      'name': 'qid record created from api sample',
                      'severity': 5,
                      'low_level_category_id': 1008
                      }

    qid_record = create_qid_record(new_qid_record)

    endpoint_url = 'data_classification/dsm_event_mappings'
    http_method = 'POST'

    new_dsm_event_mapping = {"log_source_type_id": 2,
                             "log_source_event_id": "801:1",
                             "log_source_event_category": "Auth",
                             "qid_record_id": qid_record['id']
                             }

    data = json.dumps(new_dsm_event_mapping).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 201:
        print('A new dsm event mapping is created.')
        # can extract newly created dsm event mapping from the response
        dsm_event_mapping = json.loads(response.read().decode('utf-8'))
        print(json.dumps(dsm_event_mapping, indent=4))
    else:
        print('Failed to create the new dsm event mapping')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 3. get a single dsm event mapping by id

    # id of the dsm event mapping, using dsm event mapping created in step 2
    dsm_event_mapping_id = dsm_event_mapping['id']

    endpoint_url = ('data_classification/dsm_event_mappings' + '/' +
                    str(dsm_event_mapping_id))
    http_method = 'GET'

    # Send in the request, with it printed to console
    response = client.call_api(endpoint_url, http_method, print_request=True)

    # check response and handle any error
    if response.code == 200:
        print("The requested dsm event mapping has been retrieved.")
        dsm_event_mapping = json.loads(response.read().decode('utf-8'))
        print(json.dumps(dsm_event_mapping, indent=4))
    else:
        print('Failed to retrieve the dsm event mapping with id=' +
              str(dsm_event_mapping_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 4. update a dsm event mapping by its id

    # create a new qid record for the dsm event mapping to be re-mapped to
    new_qid_record = {'log_source_type_id': 2,
                      'name': 'updated qid record',
                      'severity': 8,
                      'low_level_category_id': 1009
                      }

    updated_qid_record = create_qid_record(new_qid_record)

    # using dsm event mapping created in step 2
    dsm_event_mapping_id = dsm_event_mapping['id']

    endpoint_url = ('data_classification/dsm_event_mappings' + '/' +
                    str(dsm_event_mapping_id))
    http_method = 'POST'

    fields_to_update = {'qid_record_id': updated_qid_record['id']}

    data = json.dumps(fields_to_update).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    if response.code == 200:
        print('The dsm event mapping has been successfully updated.')
        dsm_event_mapping = json.loads(response.read().decode('utf-8'))
        print(json.dumps(dsm_event_mapping, indent=4))
    else:
        print('Failed to update the dsm event mapping with id=' +
              str(dsm_event_mapping_id))
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)


# function helps creating qid record needed for dsm event mapping
def create_qid_record(qid_record):

    client = client_module.RestApiClient(version='7.0')

    endpoint_url = 'data_classification/qid_records'
    http_method = 'POST'

    data = json.dumps(qid_record).encode('utf-8')

    headers = {'Content-type': 'application/json'}

    # send the request
    response = client.call_api(endpoint_url, http_method, data=data,
                               headers=headers, print_request=True)

    # check response and handle any error
    if response.code == 201:
        print('A new qid record is created.')
        qid_record = json.loads(response.read().decode('utf-8'))
        return qid_record
    else:
        SampleUtilities.pretty_print_response(response)
        print('Failed to create the new qid record')
        sys.exit(1)


if __name__ == "__main__":
    main()
