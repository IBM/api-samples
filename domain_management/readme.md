### Disclaimer

This repository contains samples for the `/config/domain_management/domains`
endpoints of the API. These samples are provided for reference purposes on an
"as is" basis, and are without warranties of any kind. It is strongly advised
that these samples are not run against production systems. Any issues
discovered using the samples should not be directed to QRadar support, but be
reported on the Github issues tracker.

## Domain Management API Samples

Scripts in this directory demonstrate how to use
the `/config/domain_management/domains` endpoints of the API.

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`.

You can also retrieve a list of available endpoints through the API itself
at the `/api/help/capabilities` endpoint.

The scripts in this directory include:

### 01\_GetDomain.py

`GET` endpoints for Domain API.

In the samples of this module all requests are read-only. They don't change the
current state of the domain configuration.

The samples demonstrate how to retrieve the list of all domains, how to access
an individual domain (using the default domain as an example), and what happens
when the domain being retrieved does not exist.

### 02\_DeleteDomain.py

`DELETE` endpoint for Domain API.

The sample in this module changes temporarily the current state of the domain
configuration. It does not affect the overall system functionality, since it
creates a domain with a non-existing source ID.

The sample demonstrates how to delete a domain, and what happens if the same
domain is being deleted again.

### 03\_ModifyDomain.py

`POST` endpoint for Domain API.

The samples in this module change temporarily the current state of the domain
configuration. It does not affect the overall system functionality, since they
create a domain with a non-existing source ID.

The sample demonstrates how to update a domain and verify if it has been
updated successfully.

### domainutil.py

The module contains helper methods used in the modules described above. One of
them, `setup_domain()`, demonstrates how to create a new domain using the
Domain Management API.
