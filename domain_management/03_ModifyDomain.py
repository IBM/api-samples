#!/usr/bin/env python3
"""POST endpoint for Domain API.

The samples in this module change temporarily the current state of the domain
configuration. It does not affect the overall system functionality, since they
create a domain with a non-existing source ID.
"""
import sys
from domainutil import api, pp_response, to_json, from_json, setup_domain


def update_domain(domain):
    """Returns an updated domain.

    It is only the description of the domain which is changed from empty to
    'New Description'.
    """
    domain['description'] = 'New Description'
    response = api('config/domain_management/domains/' + str(domain['id']),
                   'POST', data=to_json(domain), json=True)
    if response.code == 200:
        updated_domain = from_json(response)
        if updated_domain['description'] == 'New Description':
            print('INFO: Domain successfully updated', file=sys.stderr)
            return domain

    print('ERROR: Domain update failed', file=sys.stderr)
    pp_response(response)


def main():
    # Set up a domain to be modified below.
    domain = setup_domain()

    updated_domain = update_domain(domain)

    # Delete it now.
    api('config/domain_management/domains/' + str(updated_domain['id']),
        'DELETE')


if __name__ == "__main__":
    main()
