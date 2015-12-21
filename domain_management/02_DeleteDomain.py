#!/usr/bin/env python3
"""DELETE endpoint for Domain API.

The sample in this module changes temporarily the current state of the domain
configuration. It does not affect the overall system functionality, since it
creates a domain with a non-existing source ID.
"""
import sys
from domainutil import api, pp_response, setup_domain


def delete_domain(domain_id):
    """Deletes a domain using the given domain ID.

    If the domain with this ID has been already deleted,
    response code 404 is returned.
    """
    response = api('config/domain_management/domains/' + str(domain_id),
                   'DELETE')
    pp_response(response)


def main():
    # Set up a domain to be deleted below.
    domain = setup_domain()

    # Delete the domain.
    delete_domain(domain['id'])

    # Try to delete the same domain again. Notice the response code 404.
    delete_domain(domain['id'])


if __name__ == "__main__":
    main()
