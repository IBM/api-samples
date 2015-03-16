# QRadar API Samples 7.2.2

Code samples showing the usage of the QRadar REST API.

There is a related [Security Intelligence API Forum] to share ideas, get answers and help others.

[Security Intelligence API Forum]:https://www.ibm.com/developerworks/community/forums/html/forum?id=b02461a3-9a70-4d73-94e8-c096abe263ca&ps=25


## Introduction

This package contains sample python code that demonstrates how to use the
QRadar REST API. The API is access by sending specially crafted HTTP
requests to specific URLs on the QRadar console. These URLs, known as
`endpoints`, each perform a specific function. Some endpoints perform
different functions depending on whether you send a GET, POST, or
DELETE request. By linking together calls to these endpoints you can
implement you own custom business processes or integrate QRadar data
with external systems.

This package is applicable to version 0.1 of the reference data API, ariel API and 1.0 of the help endpoint. A version number of 1.0 is used by default by
these samples since the API automatically selects the highest version less than
or equal to the requested version.
Endpoints released as 'Provisional' or 'Experimental' may change in future
versions of the API. In general, past versions of the API remain available so
these samples will continue to run against version 0.1/1.0. When changes are
made in future versions of the API new samples will be released.

The QRadar REST API contains endpoints not covered by these samples.
Future releases of this sample package will be expanded to include
examples of more API endpoints.

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page on your QRadar
installation at https://&lt;hostname&gt;/restapi/doc
You can retrieve a list of available endpoints from the API itself at
the '/help/capabilities' endpoint.


## Package contents

- An introduction package that shows how to use the API at a low level
- A reference data package that demonstrates endpoints in the
    /referencedata category.
- An API CLI client that can be used to access the API from the
    command line.
- An Ariel package that demonstrates endpoint in the /ariel category.
- A package containing shared modules.


## Requirements

- Python 3.3 or above
- QRadar system 7.2.2 or higher


## Instructions

For the sample code to work without modifications, it is necessary that
the folder structure does not change.

To run a sample script from the command line navigate to the directory the
script is in and run `python <script_name.py>` replacing python with the 
name of your python 3 binary if it is different on your system. You can also
run these samples from your chosen python development environment as you
would run any other python script. You may need to run one sample from the
command line or set up your IDE's console to be interactive so that the
configuration file can be created.

If this is your first time running any of the samples, you will be prompted for
the configuration details. Configuration details include:

 - IP address or domain name of your QRadar install.
 - Credentials.  Either username and password or an authorized service token.
 - Optional TLS certificate.

Authorization tokens can be generated in **Authorized Services** under the
admin tab of the QRadar console.

The TLS certificate is optional, but must be provided if your system uses a
self signed TLS certificate. See the [TLS Certificate][] section for more
information.

After entering configuration details for the sample you will be prompted asking
if you would like to save the configuration to disk. If you choose to store the
configuration it will be stored in plain text unencrypted in a file called
`config.ini`. IBM recommends that you do not store sensitive credentials in
this file. If you choose not to save the configuration details in the file you
will be prompted to enter the configuration details each time you run a sample.
This configuration file is stored at the root level of the samples directory.
From there all sample scripts, as well as the command line client, will be able
to use it.

Each sample directory also contains a `Cleanup.py` script that you can use
to remove the data created by the script from your system. Some scripts
include a line that you can uncomment to clean up the script's data as soon
as it is run. Data created by scripts is left on the system by default so that
you can see how it affects the system and so that you can experiment with it
either through the API or through the main UI. IBM recommends that you clean up
this sample data when you are finished with it so that it does not get lost on
your system.

## TLS Certificate

When entering the configuration details you have the option of providing a TLS
certificate file. This is required when your QRadar system uses a self signed
certificate. When prompted enter the path to the certificate stored in PEM
format.

Use one of the following methods to obtain the certificate file:

 - Copy the certificate file from the QRadar box. The QRadar certificate is
   stored at `/etc/httpd/conf/certs/cert.cert`.
 - Export the certificate in PEM format from your browser.

When you manually obtain and specify the certificate file it is your
responsibility to verify the certificate authenticity.


## Makeup of the config.ini file

```
[DEFAULT]
server_ip = {IP ADDRESS}
auth_token = {AUTH TOKEN} (Optional)
username = {USERNAME} (Optional)
password = {PASSWORD} (Optional)
certificate_file = {CERTIFICATE FILE} (Optional)
```

If you are using the shared module `RestApiClient.py` to experiment with
writing your own API scripts there are several options available to you
for loading configurations other than the default configuration.
You can pass a different file name to have the Client load the configuration
from that file instead of the default. You can create a new configuration
section in the config.ini file and pass the name of that section.
For example you could add a section

```
[my_custom_config]
username = {my_other_username}
password = {my_other_password}
```

to the configuration file and load your setting from there. Any required setting
not included in this custom section will be loaded from the default section.
You can also create your own dictionary of setting from some other source
and pass it directly to the RestApiClient.

# ApiClient
## Instructions

These instructions assume that your python binary is called 'python'.

## AUTHORIZATION

The first time you run `apiclient.py`, you will be asked to enter configuration
information, including credentials. For more details see the Configuration
section of `readme.md`.

## USING apiclient.py

There are two main uses of apiclient.py

1. Print API endpoints.
    `python apiclient.py --print_api` will print all endpoints and information
    needed to make calls against that endpoint.
2. Make requests to an API endpoint.

### Basic api calls

The most basic call you can make is a GET request to an endpoint that requires no parameters:

```
python apiclient.py --api /help/capabilities --method GET`
```    

Arguments for basic calls:

**`--api /api_name/endpoint`** 


This is the path to your api endpoint. It is the part of the url that 
you would append to `http://<server_ip>/restapi/api`. For example 
        `http://<server_ip>/restapi/api/referencedata/sets`.
        
**`--method METHOD`**

This determines whether your api request will be a GET, POST, or 
DELETE. To know what method an endpoint needs, check the output of `--print_api`.

### Calls with path parameters

There are three types of parameters: path, query, and body parameters. 
Path parameters are those that modify the endpoint you are calling. For 
example, name is a parameter of the version 0.1 endpoint 
`/referencedata/sets/{name}`. This means that to call this endpoint
you must place the name of the set in the path to the endpoint you specify
in `--api`. For example, to retrieve a reference set identified by the name 
'exampleset'. You would call:

```
python apiclient.py --api /referencedata/sets/exampleset --method GET
```

Any path parameters will correspond to some place in endpoint portion in 
the url.

### Calls with query parameters

If you have any query parameters they must be entered with the syntax 
`--<param_name>="<param_value>"`. For example, to get all version 0.1 API 
endpoints that make use of httpMethod POST you can call 
`/help/capabilities` and supply the query parameters 'httpMethods' and 
'version'. httpMethods asks for a JSON object. We can create one 
using single quotes, squares brackets, and commas.

```
python apiclient.py --api /help/capabilities --method GET --httpMethods="['POST']" --version="0.1" 
```
    
Once again check the output of `--print_api` to determine which parameters 
are query parameters and which are body parameters.

### Calls with body parameters

Body parameters are entered in the command line the same way as query parameters `--<param_name>="<param_value>"`, except you must specify the 
content type of the body you are sending with the `--content_type TYPE` 
argument. For example, to bulkload data to an existing set of element type ALN named 'exampleset':

```
python apiclient.py --api /referencedata/sets/bulkLoad/exampleset
                    --method POST --content_type="application/json"
                    --data="['value1','value2','value3']"
```

The `--content_type` argument needs to be specified or the body will be sent 
as a query parameter and the API call will fail.

### Miscellaneous command line arguments

**`--output OUTPUT`**

This sets the 'Accept' header of the request object, determining the 
Content-type of the response object. The default is `application/json`. 
If the endpoint does not support `application/json` you will get an 
error 406 with the message:

>"MIME pattern application/json' does not match any content types 
>returned by this endpoint. This endpoint supports <content-type>" 
        
This means you must set your `--output` argument to one of the supported types.

**`--ver VER`**

This tells the system which version of the endpoint you are calling. 
If the endpoint does not have that exact version it will round down to
the closest available version number.
