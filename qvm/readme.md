# Asset Model Samples

Scripts in this directory demonstrate how to use the `/qvm/saved_searches` endpoints of the API.

For a list of the endpoints that you can use along with the parameters they
accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`
You can also retrieve a list of available
endpoints through the api itself at the `/api/help/capabilities` endpoint.


Access to the QVM API endpoints requires a user or authorized token with a
role that contains both the following privileges:
 - Assets
 - Vulnerability Management

The scripts in this directory include:

### 01_SavedSearches.py
In this sample, you see how QVM saved search data is retrieved with the QVM REST API.
For this scenario to work there must already be QVM saved searches on the system the
sample is being run against.
  
The scenario demonstrates the following actions:
- How to get QVM saved searches.
	
### 02_VulnInstancesSearchWorkFlow.py
This sample demonstrates a search workflow that is executed entirely
via the QVM REST API.

The scenario demonstrates the following actions:
- How to get specific QVM saved search.
- How to use QVM saved search to create vulnerability instances search.
- How to check current status of a vulnerability instance search.
- How to get vulnerability instances returned from a QVM saved search
- How to get assets returned from a QVM saved search
- How to get vulnerabilities returned from a QVM saved search
- How to use 'Range' header for pagination

The first call made is to get a 'High Risk' saved search.
The response includes the search id which can later be used to create the
vulnerability instance search.

The 2nd call made is to create a vulnerability instances search using the search id.
Since searches are executed asynchronously, the API call to begin the search
returns immediately. The response is parsed to extract the task id. The task id is then used to retrieve the status of the search using the API. If the search is not complete, it 
will continue to call the API until the search status is either an error, timeout or complete.
 
Once the search completes, retrieve the vulnerability instances results of the search using pagination.  Get 10 rows of vulnerability instances results at a time until we get a total of 30 rows back.

Within each iteration (i.e. 10 rows of vulnerability instances results), build a set of associated asset IDs and a set of vulnerability IDs.  Use the set of asset IDs as a filter to call API to get assets results.  Use the set of vulnerability IDs as a filter to call API to get vulnerabilities results.