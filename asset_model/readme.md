# Asset Model Samples

Scripts in this directory demonstrate how to use the `/asset_model` endpoints of the API.

For a list of the endpoints that you can use along with the parameters they
accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`
You can also retrieve a list of available
endpoints through the api itself at the `/api/help/capabilities` endpoint.


Access to the Assets API endpoints requires a user or authorized token with a
role that contains both the following privileges:
 - Assets


The scripts in this directory include:

### 01_GetAssets.py
In this sample, you see how asset data is retrieved with the assets REST API.
For this scenario to work there must already be assets on the system the
sample is being run against.  
The scenario demonstrates the following actions:
- How to get assets.
	
### 02_GetProperties.py
In this sample, you see how available asset property data is retrieved with the assets REST API.  
The scenario demonstrates the following actions:
- How to get available asset properties.	

### 03_GetSavedSearches.py	
In this sample, you see how available saved searches are retrieved with the assets REST API.  
The scenario demonstrates the following actions:
- How to get available saved searches.		
	
### 04_SearchAssets.py
In this sample, you see how available saved searches are used to retrieve asset data with the assets REST API.
For this scenario to work there must already be assets on the system the sample is being run against.  
The scenario demonstrates the following actions:   
- How to get available saved searches.
- How to use a saved search against assets.
