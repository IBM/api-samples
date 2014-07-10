Scripts in this directory serve as an introduction to using the API.
Basics such as how to authenticate with the system, how to
pass various types of parameters, and an introduction to the
types of errors you might encounter are covered here.
These samples use reference data endpoints (/referencedata) to demonstrate
this functionality.

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page at
https://<hostname>/restapi/doc
You can also retrieve a list of available endpoints through the api itself
at the /api/help/capabilities endpoint.


The scripts in this directory include:

01_Authentication.py
 - This sample demonstrates how to encode credentials, how to format and
 - attach headers to an HTTP request, and how to send a simple request
 - to a REST API endpoint.

02_QueryParameters.py
 - This sample demonstrates how to use query parameters with a REST API
 - endpoint.

03_PathParameters.py
 - This sample shows how to use path parameters with the REST API.

04_BodyParameters.py
 - This sample demonstrates how to send a parameter in the body of a
 - request.

05_Errors.py
 - This sample demonstrates some common errors that can be made while
 - using the REST API. It shows the information that is returned with
 - an error response to help you diagnose the problem.

 
