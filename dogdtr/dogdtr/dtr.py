import json
import urllib

from requests import RequestException
from requests import get
from typing import List, Tuple, Union


from .utils import MIMEType


class DataTypeNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


def expand_datatype(data_type: Union[str, List[str]]) -> List[dict]:
    """
    Wrapper for DTR datatype taxonomy discovery
    """
    if isinstance(data_type, str):
        return [get_dtr_taxonomy_by_type(data_type)]
    elif isinstance(data_type, list):
        return [get_dtr_taxonomy_by_type(dt) for dt in data_type]


def get_dtr_taxonomy_by_type(data_type: str) -> dict:
    """
    Returns a dictionary representation of the MIME type taxonomy

    :param data_type: str, MIME type, e.g. 'text/xml'
    :return: dict, a dictionary representation of the type's taxonomy
    """
    dtr_taxonomy_search_endpoint = f"http://typeapi.lab.pidconsortium.net/v1/taxonomy/search?query={data_type}&name={data_type}"
    data_type = urllib.parse.quote(data_type, safe='')

    try:
        dtr_taxonomy_search_response = get(dtr_taxonomy_search_endpoint)
    except RequestException as error:
        raise DataTypeNotFoundException(f"Failed to reach DTR to query for taxonomy") from error
    except ValueError as error:
        raise DataTypeNotFoundException(f"Failed to unpack DTR response. Most probably {data_type} is not registered") from error

    try:
        dtr_taxonomy_search_json = dtr_taxonomy_search_response.json()
        type_taxonomy_id = dtr_taxonomy_search_json[0]["id"]
    except IndexError as error:
        raise DataTypeNotFoundException(f"Failed to resolve {data_type} taxonomy. Most probably it doesn't exist.")


    root_taxonomy_id = retrieve_root(type_taxonomy_id)
    taxonomy_tree = retrieve_taxonomy_tree(root_taxonomy_id)
    return taxonomy_tree

def retrieve_root(taxonomy_id: str) -> Tuple[str, str]:
    dtr_taxonomy_endpoint = f"http://typeapi.lab.pidconsortium.net/v1/taxonomy/{taxonomy_id}"
    taxonomy_response = get(dtr_taxonomy_endpoint)
    taxonomy_json = taxonomy_response.json()

    # Recurse until no parent under "parents" key
    for parent_id, parent_name in taxonomy_json["parents"].items():
        return retrieve_root(parent_id)
    taxonomy_id = taxonomy_json["id"]
    return taxonomy_id


def retrieve_taxonomy_tree(taxonomy_id: str):
    dtr_taxonomy_endpoint = f"http://typeapi.lab.pidconsortium.net/v1/taxonomy/{taxonomy_id}"
    dtr_taxonomy_response = get(dtr_taxonomy_endpoint)
    dtr_taxonomy_json = dtr_taxonomy_response.json()

    taxonomy_name = dtr_taxonomy_json["name"]

    children = []
    for child_id, child_name in dtr_taxonomy_json["children"].items():
        children.append(retrieve_taxonomy_tree(child_id))
    return {taxonomy_name: {"id": taxonomy_id, "children": children}}


"""
OLD TAXONOMY DISCOVERY IMPLEMENTATION
"""
# class TaxonomyNode:
#     def __init__(self, pid: str, data_type: str, children: list = None, parents: list = None):
#         self.children: List[TaxonomyNode] = [] if children is None else children
#         self.data_type: str = data_type
#         self.parents: List[TaxonomyNode] = [] if parents is None else parents
#         self.pid: str = pid
#         self.dtr_taxonomy_endpoint: str = f"http://typeapi.lab.pidconsortium.net/v1/taxonomy/{self.pid}"
#
#     def dtr_type_query(self) -> dict:
#         url, dtr_taxonomy_search_response, header = get(self.dtr_taxonomy_endpoint)
#         dtr_taxonomy_json: dict = json.loads(dtr_taxonomy_search_response)
#         return dtr_taxonomy_json
#
#     def populate_relatives(self, relatives: Union[str, Set[str]]) -> "TaxonomyNode":
#         dtr_taxonomy_json: dict = self.dtr_type_query()
#         if "children" in relatives:
#             for child_pid, child_name in dtr_taxonomy_json["children"].items():
#                 child_node = TaxonomyNode(child_pid, child_name)
#                 child_node.populate_relatives("children")
#                 self.add_child(child_node)
#         if "parents" in relatives:
#             for parent_pid, parent_name in dtr_taxonomy_json["parents"].items():
#                 parent_node = TaxonomyNode(parent_pid, parent_name)
#                 parent_node.populate_relatives("parents")
#                 self.add_parent(parent_node)
#
#     def add_child(self, child: "TaxonomyNode"):
#         self.children.append(child)
#
#     def add_parent(self, parent: "TaxonomyNode"):
#         self.parents.append(parent)


# def get_dtr_taxonomy(data_type: str, relatives: Union[str, Set[str]]) -> TaxonomyNode:
#     dtr_taxonomy_search_endpoint = f"http://typeapi.lab.pidconsortium.net/v1/taxonomy/search?query={data_type}&name={data_type}"
#     url, dtr_taxonomy_search_response, header = get(dtr_taxonomy_search_endpoint)
#     dtr_taxonomy_json = json.loads(dtr_taxonomy_search_response)
#     try:
#         root_id = dtr_taxonomy_json[0]["id"]
#         root_name = dtr_taxonomy_json[0]["name"]
#     except KeyError as error:
#         raise DataTypeNotFound(f"DataType <{data_type}> doesn't exist in the DTR taxonomy") from error
#
#     taxonomy_node = TaxonomyNode(root_id, root_name)
#     taxonomy_node.populate_relatives({"children", "parents"})
#     return taxonomy_node
