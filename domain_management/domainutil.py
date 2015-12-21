"""Domain utilities used by sample scripts for Domain API.
"""
import json
import os
import sys
import uuid
from importlib import import_module

sys.path.append(os.path.realpath('../../modules'))

_RestApiClient = import_module('RestApiClient')
_SampleUtilities = import_module('SampleUtilities')
_client = _RestApiClient.RestApiClient(version='5.0')


# Pretty-prints response.
pp_response = _SampleUtilities.pretty_print_response


def api(endpoint, method, data=None, json=False):
    """Invokes RestApiClient call_api method and pretty-prints the request.
    """
    if json:
        headers = _client.get_headers().copy()
        headers['Content-type'] = 'application/json'
    else:
        headers = None

    return _client.call_api(endpoint, method, headers=headers, data=data,
                            print_request=True)


def from_json(response):
    """Converts RestApiClient response from JSON to string.
    """
    return json.loads(response.read().decode('utf-8'))


def to_json(data):
    """Converts Python data to JSON.
    """
    return json.dumps(data).encode('utf8')


def setup_domain():
    """Sets up a domain with event collector ID = -1000 and returns this new
    domain.

    The domain name is a randomly generated UUID. The event collector ID is
    chosen to be not among existing IDs.

    If the data for the event collector ID already exists, re-use the domain
    with that event collector configured.
    """
    body = {
        "asset_scanner_ids": [],
        "custom_properties": [],
        "deleted": False,
        "description": "",
        "event_collector_ids": [-1000],  # Assign non-existing ID
        "flow_collector_ids": [],
        "flow_source_ids": [],
        "log_source_group_ids": [],
        "log_source_ids": [],
        "name": str(uuid.uuid4()),  # Generate a random domain name
        "qvm_scanner_ids": [],
        "tenant_id": 0
    }

    response = api('config/domain_management/domains', 'POST',
                   data=to_json(body), json=True)

    if response.code == 201:
        return from_json(response)
    elif response.code == 409:
        # Finds the domain ID for conflicting resource.
        resp = api('config/domain_management/domains', 'GET')
        domains = from_json(resp)
        for domain in domains:
            if -1000 in domain['event_collector_ids']:
                return domain
    print('ERROR: Unrecognized conflict error', file=sys.stderr)
