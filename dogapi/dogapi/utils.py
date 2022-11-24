from rest_framework.request import Request
from typing import List


class QueryparamParsingError(Exception):
    """
    Raised when unable to parse given query parameter from the request

    :param param_name: name of query parameter to parse
    :type param_name: str
    :param message: error message to be displayed
    :type message: str, optional

    """
    def __init__(self, param_name: str, message="Could not parse parameter value from the query"):
        self.message = message
        self.param_name = param_name
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.param_name}'


def parse_queryparam(request: Request, param_name: str) -> List[str]:
    """
    Parses list of queryparameters from direct API call (PHP-like format ?param[]=val1&param[]=val2,
    both with and without []) and via Swagger UI (?param=val1,val2)

    :param request: instance of Django REST Framework Request
    :type request: rest_framework.request.Request
    :param param_name: name of the query parameter to be parsed from request
    :type param_name: str

    :raises QueryparamParsingError: raised when unable to parse named query parameter from request

    :return: list of parameter values parsed from request
    :rtype: List[str]
    """
    query_pid_candidates = request.query_params.getlist(f'{param_name}')

    # check if pid parameter passed
    if query_pid_candidates is None:
        # try parsing PHP-like format for queryparam list
        query_pid_candidates = request.query_params.getlist(f'{param_name}[]')
        if query_pid_candidates is None:
            raise QueryparamParsingError(param_name)

    # Swagger UI returns a 1 element list with comma separated values of parameter, e.g. ["string,string,string"]
    pid_candidates = [pid for pid_candidate in query_pid_candidates for pid in pid_candidate.split(',')]
    return pid_candidates
