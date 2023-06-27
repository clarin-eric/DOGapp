# DOGapp
DOGapp is a modelless Django application exposing REST API for [DOGlib](https://github.com/clarin-eric/DOGlib) functionalities. 
Its goal is to provide fair access to CLARIN resources from the metadata by exposing both UI interface and API endpoints. 

## API
PID's can be passed as parameters to URL query in following formats:
>?pid=val1&pid=val2&pid=val3 \
>?pid=val1,val2,val3 \
>?pid[]=val1&pid[]=val2

Available endpoints:

`/api/schema`, provides OpenApi 3.0 specification of the API.

`/api/sniff/?pid`, Checks whether PID points to resources in registered repository.

`/api/fetch/?pid`, Fetches all PIDs referenced in the metadata, supports PID and list of PIDs to metadata in formats.

`/api/identify/?pid`, identifies PID (VLO request).

## Installation
Install packages by running following commands in the project's root dir (order matters):
```bash
pip install ./dogapi
pip install ./dogui
pip install ./dogconfig
```

## Testing
In order to run the unittests simply run
```bash
python ./runtests.py
```
in the project's root directory. The script will take care of providing minimal testing configuration and testing all the applications

## Running
To start the project local installation of `dogapi` and `dogui` is required, config can be spinned from source by running
```bash
python ./dogconfig/manage.py runserver
```