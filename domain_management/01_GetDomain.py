#!/usr/bin/env python3
"""GET endpoints for Domain API.

In the samples of this module all requests are read-only. They don't change the
current state of the domain configuration.
"""
import sys
from domainutil import api, from_json, pp_response


def get_all_domains():
    """Retrieves the list of all domains and prints their total number and
    the number of active domains.

    The number of the domains must be always greater than zero,
    since the default domain is always in the list of the returned domains.
    """
    response = api('config/domain_management/domains', 'GET')
    response_body = from_json(response)

    print('INFO: Number of all domains retrieved: ' + str(len(response_body)))

    # Now count only active domains.
    num = sum(map(lambda d: d['deleted'] is False, response_body))
    print('INFO: Number of active domains retrieved: ' + str(num))


def get_default_domain():
    """Retrieves the default domain from the list of all domains.

    The default domain always exists.
    Any other domain is retrieved the same way.
    """
    response = api('config/domain_management/domains/0', 'GET')
    pp_response(response)


def get_non_existing_domain():
    """Tries to retrieve a domain that does not exist... and fails with code 404.
    """
    response = api('config/domain_management/domains/-1', 'GET')
    if response.code == 404:
        pp_response(response)
    else:
        print('ERROR: Response code 404 was expected', file=sys.stderr)
        sys.exit(1)


def main():
    get_all_domains()
    get_default_domain()
    get_non_existing_domain()


if __name__ == "__main__":
    main()
