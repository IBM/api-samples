## Offense API Sample
Scripts in this directory demonstrate how to use the offense endpoints (/siem
category) of the API.


For a list of the endpoints that you can use along with the parameters they
accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`.  You can also retrieve a list of available
endpoints through the api itself at the /api/help/capabilities endpoint.


Access to the Offense API endpoints requires a user or authorized token with a
role that contains both the following privileges:
 * Offenses
 * siem API


The scripts in this directory include:

01_GetOffenses.py
 In this sample, you see how offense data is retrieved with the offense REST
   API.
 For this scenario to work there must already be offenses on the system the
 sample is being run against.  

The scenario demonstrates the following actions:
* How to get offenses.
* How to page through the results using the limit and offset parameters.
* How to filter the data that is returned with the fields parameter.
