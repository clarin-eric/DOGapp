# DOGapp
DOGapp is a Django application providing REST API for DOGlib functionalities

## API
`/sniff/?pid`, where pid is a PID-like string. Accepts URL, HDL, DOI. Returns PID's host information.

`/fetch/?pid`, where pid is a PID-like string. Accepts URL, HDL and DOI. Resolves the collection and returns collection of all referenced resources. 

Both calls come as well in a bulk form. In order to process multiple PIDs at the same time use POST and pass a list of PIDs in data under a key `pids`, e.g. using Curl:

`curl --insecure -X POST https://localhost:8000/fetch_bulk/ -d '{"pids":["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3698", "http://hdl.handle.net/1839/00-0000-0000-0018-A640-9"]}' -H "Content-Type: application/json
