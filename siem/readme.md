This repository contains samples for the `siem` endpoint of the API.

These samples are provided for reference purposes on an "as is" basis, and are without warranties of any kind.

Any issues discovered using the samples should not be directed to QRadar support, but be reported on the Github issues tracker.

# Siem Samples
Scripts in this directory demonstrate how to use the `siem` endpoints of the API.


For a list of the endpoints that you can use along with the parameters they
accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`.  You can also retrieve a list of available
endpoints through the api itself at the /api/help/capabilities endpoint.


Access to the Offense API endpoints requires a user or authorized token with a
role that contains both the following privileges:

 * Offenses
 * `siem` API


The scripts in this directory include:

### 01_GetOffenses.py
In this sample, you see how offense data is retrieved with the `siem` API, and how to use
the `fields` and `filter` parameters and the `Range` header to make the data retrieved concise
and easy to read.  
For this scenario to work there must already be offenses on the system the
sample is being run against.  
The scenario demonstrates the following actions:

- How to get offenses.
- How to filter the data that is returned with the `fields` parameter.
- How to filter the data that is returned with the `filter` parameter.
- How to page through the results using the `Range` parameter.

### 02_HideOffenses.py
In this sample, you see how to retrieve offenses and have the user select one, and
retrieve information from that offense. The sample concludes by showing how to change
the status of an offense using the `POST` endpoint and the `status` field.  
For this scenario to work there must already be offenses on the system the
sample is being run against.  
**This sample will make changes to the offense it is run against.**  
The scenario demonstrates the following actions:

- How to get offenses with the status `OPEN` using the `filter` parameter
- How to get a single offense given the ID
- How to decode data received and access the information
- How to hide an offense

### 03_ShowOffense.py
This sample shows how to "show" an offense as specified by QRadar. It operates in
a manner similar to sample 02.  
For this scenario to work there must already be offenses on the system the
sample is being run against.  
**This sample will make changes to the offense it is run against.**  
The scenario demonstrates the following actions:

- How to get offenses with the status `HIDDEN` using the `filter` parameter
- How to get a single offense given the ID
- How to decode data received and access the information
- How to show an offense

### 04_Notes.py
In this sample, you see how notes on offenses work, and how to display notes and
create new ones using the `siem` API.  
For this scenario to work there must already be offenses on the system the
sample is being run against.  
**This sample will make changes to the offense it is run against.**  
The scenario demonstrates the following actions:

- How to get offenses
- How to get a single offense given the ID
- How to get notes from an offense
- How to make a new note for an offense

### 05_ClosingReasons.py
This sample shows how to display closing reasons, and create custom ones.
**This sample will make changes to the offense it is run against.**  
The scenario demonstrates the following actions:

- How to get a list of closing reasons
- How to create a new closing reason

### 06_ClosingAnOffense
In this scenario we will be closing an offense in a system similar to how the
the user can close offenses in QRadar. This has four main processes.

  1. Select an offense
  2. Select a closing reason
  3. Modify `status` to `CLOSED`
  4. Leave a note

For this scenario to work there must already be offenses on the system the
sample is being run against.  
**This sample will make changes to the offense it is run against.**  
The scenario demonstrates the following actions:

- Using `filter` and `field` parameters with `GET` endpoints to retrieve a comprehensive list
- Selecting objects with `GET` from known lists of things with specific properties
- How to post notes on an offense
- How to close an offense
