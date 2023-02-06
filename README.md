# DOGapp
DOGapp is a modelless Django application exposing REST API for [DOGlib](https://github.com/clarin-eric/DOGlib) functionalities. 
Its goal is to provide fair access to CLARIN resources from the metadata by exposing both UI interface and API endpoints. 

## API
PID's can be passed as parameters to URL query in following formats:
>?pid=val1&pid=val2&pid=val3 \
>?pid=val1,val2,val3

`/api/sniff/?pid`, Checks whether PID points to resources in registered repository.

`/api/fetch/?pid`, Fetches all PIDs referenced in the metadata, supports PID and list of PIDs to metadata in formats.

`/api/identify/?pid`, identifies PID (VLO request).

`/api/swagger.json`, provides OpenApi 2.0 specification of the API.
