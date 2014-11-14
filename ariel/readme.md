## Ariel Samples 
This repository contains samples for the `ariel` endpoint of the API.

These samples are provided for reference purposes on an "as is" basis, and are without warranties of any kind.

It is strongly advised that these samples are not run against production systems.

Any issues discovered using the samples should not be directed to QRadar support, but be reported on the Github issues tracker.

Scripts in this directory demonstrate how to use the ariel 
endpoints (/ariel) of the API.

The samples have been updated to use [Ariel V3 query language](
http://public.dhe.ibm.com/software/security/products/qradar/documents/7.2.3/QRadar/EN/b_qradar_aql.pdf)

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page at
https://&lt;hostname&gt;/api_doc

You can also retrieve a list of available endpoints through the api itself
at the '/api/help/capabilities' endpoint.


The scripts in this directory include:

### 01_ArielAPIFaultyQuery.py
  This sample demonstrates what will happen when an invalid
  AQL query is submitted by a user. In this case, the field 'foobar', which 
  does not exist in the 'events' catalog (database), is being selected.
  This will result in a failure to evaluate the query.


### 02_ArielAPIGetDatabases.py
 This sample demonstrates how to retrieve a list of all available catalogs 
 (databases) that can be queried using AQL through the API. 


### 03_ArielAPISearchWorkFlow.py
 This sample demonstrates a search workflow that is executed entirely
 via the ariel API.
 
 The first call made is to submit a search with a simple AQL statement.
 Since searches are executed asynchronously, the API call to begin the search
 returns immediately. The response includes the search id which can 
 later be used to retrieve the status and/or results of the search.
 
The response is parsed to extract the search id. The search id is then used to 
retrieve the status of the search using the API. If the search is not complete, it 
will continue to call the API until the search status is either an error or complete.
 
Once the search completes, we retrieve the results of the search in JSON format
and print them out. Then we make the same call to retrieve results, but this time
in CSV format.
 
Lastly, a call is made to the API in order to save the results of the search to disk
permanently. This ensures that the search is not automatically removed when it expires 
in accordance with the retention policy. 
