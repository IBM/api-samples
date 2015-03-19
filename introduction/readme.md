These samples are provided for reference purposes on an "as is" basis, and are without warranties of any kind.

It is strongly advised that these samples are not run against production systems.

Any issues discovered using the samples should not be directed to QRadar support, but be reported on the Github issues tracker.

# Introductory Samples

Scripts in this directory serve as an introduction to using the API.
Basics such as how to authenticate with the system, how to
pass various types of parameters, and an introduction to the
types of errors you might encounter are covered here.
These samples use `reference_data` endpoints to demonstrate
this functionality.

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`  
You can also retrieve a list of available endpoints through the api itself
at the `/api/help/capabilities` endpoint.


The scripts in this directory include:

### 01_Authentication.py
This sample demonstrates how to encode credentials, how to format and
attach headers to an HTTP request, and how to send a simple request
to a REST API endpoint.

### 02_QueryParameters.py
This sample demonstrates how to use query parameters with a REST API
endpoint.

### 03_PathParameters.py
This sample shows how to use path parameters with the REST API.

### 04_BodyParameters.py
This sample demonstrates how to send a parameter in the body of a
request.

### 05_Errors.py
This sample demonstrates some common errors that can be made while
using the REST API. It shows the information that is returned with
an error response to help you diagnose the problem.

### 06_CommonParameters.py
In this sample you will see how to limit the data returned by an endpoint
using some shared parameters. The `filter` query parameter can be used to
restrict the elements returned in a list based on the contents of the fields
being returned. The `Range` header parameter can be used to page the elements
of a list by specifying the start and end values of the range you want. the
`fields` query parameter is used to specify the fields in the return object
you are interested in. Only those fields will be returned in the response.
This sample uses the `reference_data/sets` endpoints as an example, but these
parameters can be applied to many other endpoints.

### 07_DeprecatedHeader.py
This sample demonstrates the Deprecated response header. The Deprecated
response header is returned any time a deprecated version of the API is
called.
