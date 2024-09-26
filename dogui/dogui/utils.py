import django_dataclasses
from doglib import FetchResult, ReferencedResource, ReferencedResources


@django_dataclasses.dataclass
class FetchResultWrapper:
    """Wrapping dict of dataclasses into django_dataclasses.dataclass,
    because Django is retarded and can't use dictionary as dictionary"""
    pid: str
    fetch_result: FetchResult


class TaxonomyTree:
    def __init__(self, taxonomy_dict: dict):
        self.name = next(iter(taxonomy_dict.keys()))
        taxonomy_dict = taxonomy_dict[self.name]
        tree_root_pid: str = ""
        for node_pid, taxonomy_node in taxonomy_dict.items():
            if not taxonomy_node["parents"]:
                tree_root_pid = node_pid
                break
        self.node = TaxonomyNode(tree_root_pid, taxonomy_dict)


class TaxonomyNode:
    def __init__(self, pid: str, taxonomy_dict: dict):
        self.children: list = []
        self.has_children: bool
        self.name = taxonomy_dict[pid]["name"]
        self.pid = pid
        for child_id in taxonomy_dict[pid]["children"]:
            self.children.append(TaxonomyNode(child_id, taxonomy_dict))
        self.has_children = self._has_children()

    def _has_children(self) -> bool:
        return True if self.children else False

