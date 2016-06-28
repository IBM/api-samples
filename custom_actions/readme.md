# Custom Actions Samples

Scripts in this directory demonstrate how to use the `/analytics/custom_actions` endpoints of the API.

For a list of the endpoints that you can use along with the parameters they
accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`
You can also retrieve a list of available
endpoints through the api itself at the `/api/help/versions` endpoint.

Access to the Custom Actions API endpoints is restricted to admin users.

The scripts in this directory include:

### 01_getCustomActionInterpreters.py
In this sample, you see how available custom action interpreters 
are retrieved with the custom actions REST API.
The scenario demonstrates the following actions:
- How to retrieve all custom action interpreters.
- How to retrieve specific custom action interpreters.
	
### 02_GetCustomActionScripts.py
In this sample, you see how available custom action scripts 
are retrieved with the custom actions REST API. For the scenario 
to work there must be custom action scripts on the system the sample is run against. 
The scenario demonstrates the following actions:
- How to retrieve all custom action scripts.
- How to retrieve specific custom action scripts.
	
### 03_getCustomActions.py	
In this sample, you see how available custom actions
are retrieved with the custom actions REST API. For the scenario 
to work there must be custom actions on the system the sample is run against.  
The scenario demonstrates the following actions:
- How to retrieve all custom actions.
- How to retrieve specific custom actions.
	
### 04_postCustomActions.py
In this sample, you see how custom action scripts and custom actions are posted to the system 
and updated on the system. 
WARNING: This sample makes changes to the QRadar system and it is 
recommended that it is not run against a production system.
The scenario demonstrates the following actions:   
- How to post custom action scripts to the system.
- How to update existing scripts on the system.
- How to post custom actions to the system.
- How to update existing custom actions on the system.

### 05_deleteCustomActions.py
In this sample, you will see how custom action scripts and custom actions are deleted from the system.
This sample will remove all custom action scripts and custom actions from the QRadar system. It is
recommended that it is not run against a production system.
The scenario demonstrates the following actions:
- How to delete custom action scripts from the system.
- How to delete custom actions from the system.

The custom_action_samples directory contains simple custom action script samples which demonstrate how parameters
are passed in each language. The custom action created from 04_postCustomActions.py can be run from the test
execution screen accessed from the 'Define Actions' admin panel. Custom action scripts must be deployed from
the admin tab before they can be executed.
