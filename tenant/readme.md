These samples are provided for reference purposes on an "as is" basis, and are without warranties of any kind.

It is strongly advised that these samples are not run against production systems.

Any issues discovered using the samples should not be directed to QRadar support, but be reported on the Github issues tracker.

# Introductory Samples

Scripts in this directory serve as an introduction to using the API.
Basics such as how to authenticate with the system, how to
pass various types of parameters, and an introduction to the
types of errors you might encounter are covered here.

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`  
You can also retrieve a list of available endpoints through the api itself
at the `/api/help/capabilities` endpoint.


The scripts in this directory include:

### 01_GetTenant.py
This sample demonstrates how to retrieve the list of tenant, and how to send a simple request
to a REST API endpoint.

### 02_CreateUpdateDeleteTenant.py
This sample demonstrates how to create, modify and delete a tenant with a REST API
endpoint.

