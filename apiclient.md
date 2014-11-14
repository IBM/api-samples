﻿# Instructions

These instructions assume that your python binary is called **"python"**.

## AUTHORIZATION

The first time you run `apiclient.py`, you will be asked for either a username and
password, or an authorization token. Authorization tokens must be generated on
the system whose API you are calling. After your credentials are entered, your 
configuration will be tested. If your configuration is valid, it will write 
your configuration to a `config.ini` file found in the same folder. Information 
on modifying `config.ini` files can be found at the end of this document.

## USING apiclient.py

There are two main uses of apiclient.py

1. Print API endpoints.

* `python apiclient.py --print_api` will print all endpoints and information
needed to make calls against that endpoint.

2. Make requests to an API endpoint.

## Basic api calls

The most basic call you can make is a GET request to an endpoint that 
requires no parameters:

        python apiclient.py --api /help/capabilities --method GET

Arguments for basic calls: 

```
--api /api_name/endpoint 
```

* This is the path to your api endpoint. It is the part of the url that 
you would append to `http://<server_ip>/restapi/api`. For example 
`http://<server_ip>/restapi/api/referencedata/sets`.

```
--method METHOD
```

* This determines whether your api request will be a GET, POST, or 
DELETE. To know what method an endpoint needs, check the output of 
`--print_api`.

## Calls with path parameters

There are three types of parameters. path, query, and body parameters. 
Path parameters are those that modify the endpoint you are calling. For 
example, name is a parameter of the ver 0.1 endpoint 
`/referencedata/sets/{name}`. This means, to call this endpoint, 
you must place the name of the set in the path to the endpoint you specify
in `--api`. For example, to retrieve a reference set identified by the name 
`exampleset`. You would call:

    python apiclient.py --api /referencedata/sets/exampleset --method GET

Any path parameters will correspond to some place in endpoint portion in 
the url.

## Calls with query parameters

If you have any query parameters, they must be entered with the syntax 
`--params <param_name>="<param_value>"`. For example, to get all 
API endpoints of `/help` that make use of httpMethod GET, 
you can call `/help/capabilities` and supply the query parameters 
`httpMethods` and `categories`. Since httpMethods asks for a JSON object, 
we can create one inside double quotes using single quotes, squares 
brackets, and commas.

    python apiclient.py --api /help/capabilities --method GET
        --params httpMethods="['GET']" categories="['/help']"

Once again check the output of `--print_api` to determine which parameters 
are query, or body parameters.

## Calls with body parameters

Body parameters are entered in the command line the same way as query 
parameters, `--<param_name>="<param_value>"`, except you must specify the 
content type of the body you are sending with the `--content_type TYPE` 
argument. For example, to bulkload data to an existing set of element type 
ALN named `exampleset`:

    python apiclient.py --api /referencedata/sets/bulkLoad/exampleset
        --method POST --content_type="application/json"
        --params data="['value1','value2','value3']"

The `--request_format` argument needs to be specified or the body will be sent 
as a query parameter, and the API call will fail.

## Miscellaneous command line arguments

```
--response_format RESPONSE_FORMAT
```

This sets the `Accept` header of the request object, determining the 
Content-type of the response object. The default is `application/json`. 
If the endpoint does not support `application/json` you will get an 
error 406 with the message:
            "MIME pattern 'application/json' does not match any content types 
            returned by this endpoint. This endpoint supports <content-type>" 
This means you must set your `--response_format` argument to one of the 
supported types.

```
--version VERSION
```

This tells the system which version of the endpoint you are calling. 
If the endpoint does not have that exact version it will round down to
the closest available version number.

```
--range RANGE
```

If an endpoint supports paging, you can supply the range of items you 
would like to have returned with `--range x-y`.


## Modifying the config.ini file 

For the apiclient to run properly it requires a server_ip and proper 
authorization. The authorization can either be an auth_token or a username and
password. 

Template config.ini #1: With authorization token

```
[DEFAULT]
server_ip = {IP ADDRESS}
auth_token = {AUTH TOKEN}
```

Template config.ini #2: With username and password.

```
[DEFAULT]
server_ip = {IP ADDRESS}
username = {USERNAME}
password = {PASSWORD}
```

Nothing else needs to be specified in the config.ini file.
