from django.conf import settings
from typing import Literal

from dogapi.utils import parse_queryparam


API_NETLOC = settings.NETLOC


def get_api_call_url(request, functionality: Literal["fetch", "sniff", "identify", "ispid"]) -> str:
    query_params = parse_queryparam(request, 'pid')
    api_call_url: str = API_NETLOC + f"/{functionality}/?pid=" + ','.join(query_params)
    return api_call_url
