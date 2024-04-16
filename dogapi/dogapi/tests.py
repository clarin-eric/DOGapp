from django.test import Client
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
import unittest

from dogapi.utils import parse_queryparam

from .models import dog


class TestQueryParamParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request_factory: APIRequestFactory = APIRequestFactory()
        cls.single_pid = ['val1']
        cls.triple_pid = ['val1', 'val2', 'val3']

    def test_php_params_with_brackets(self):
        request_single_pid: Request = self.request_factory.get('/fetch/?pid[]=val1')
        request_triple_pid: Request = self.request_factory.get('/fetch/?pid[]=val1&pid[]=val2&pid[]=val3')

        self.assertTrue(parse_queryparam(request_single_pid, "pid") == self.single_pid and
                        parse_queryparam(request_triple_pid, "pid") == self.triple_pid)

    def test_php_params_without_brackets(self):
        request_single_pid: Request = self.request_factory.get('/fetch/?pid=val1')
        request_triple_pid: Request = self.request_factory.get('/fetch/?pid=val1&pid=val2&pid=val3')

        self.assertTrue(parse_queryparam(request_single_pid, "pid") == self.single_pid and
                        parse_queryparam(request_triple_pid, "pid") == self.triple_pid)

    def test_swagger_params_format(self):
        request_single_pid: Request = self.request_factory.get('/fetch/?pid=val1')
        request_triple_pid: Request = self.request_factory.get('/fetch/?pid=val1,val2,val3')

        self.assertTrue(parse_queryparam(request_single_pid, "pid") == self.single_pid and
                        parse_queryparam(request_triple_pid, "pid") == self.triple_pid)


class TestFetchEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.dog = dog

    def test_single_correct_pid(self):
        pid = "https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"
        response = self.client.get(f"/api/fetch/?pid={pid}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertFalse(response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"])

    def test_multiple_correct_pid(self):
        pids = ["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422", "https://b2share.eudat.eu/records/d64361c0a6384760a8a8f32e0dc4a481"]
        response = self.client.get(f"/api/fetch/?pid={','.join(pids)}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertFalse(
            response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"] and
            response.json()["https://b2share.eudat.eu/records/d64361c0a6384760a8a8f32e0dc4a481"]["failure"])

    def test_single_incorrect_pid(self):
        pid = "abcd"
        response = self.client.get(f"/api/fetch/?pid={pid}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertTrue(response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"])

    def test_multiple_incorrect_pid(self):
        pids = ["abcd", "efgh"]
        response = self.client.get(f"/api/fetch/?pid={','.join(pids)}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertTrue(response.json()["abcd"]["failure"] and
                        response.json()["efgh"]["failure"])

    def test_mixed_correct_incorrect_pid(self):
        pids = ["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422", "abcd"]
        response = self.client.get(f"/api/fetch/?pid={','.join(pids)}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertTrue(
            not response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"]
            and response.json()["abcd"]["failure"])
        

class TestSniffEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.dog = dog

    def test_single_correct_pid(self):
        pid = "https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"
        response = self.client.get(f"/api/sniff/?pid={pid}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertFalse(response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"])

    def test_multiple_correct_pid(self):
        pids = ["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422", "https://b2share.eudat.eu/records/d64361c0a6384760a8a8f32e0dc4a481"]
        response = self.client.get(f"/api/sniff/?pid={','.join(pids)}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertFalse(
            response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"] and
            response.json()["https://b2share.eudat.eu/records/d64361c0a6384760a8a8f32e0dc4a481"]["failure"])

    def test_single_incorrect_pid(self):
        pid = "abcd"
        response = self.client.get(f"/api/sniff/?pid={pid}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertTrue(response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"])

    def test_multiple_incorrect_pid(self):
        pids = ["abcd", "efgh"]
        response = self.client.get(f"/api/sniff/?pid={','.join(pids)}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertTrue(response.json()["abcd"]["failure"] and
                        response.json()["efgh"]["failure"])

    def test_mixed_correct_incorrect_pid(self):
        pids = ["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422", "abcd"]
        response = self.client.get(f"/api/sniff/?pid={','.join(pids)}")
        # if correct failure code will be 0, note that 200 response code does not imply success
        self.assertTrue(
            not response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]["failure"]
            and response.json()["abcd"]["failure"])


class TestIsPIDEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.dog = dog

    def test_single_correct_pid(self):
        pid = "https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"
        response = self.client.get(f"/api/ispid/?pid={pid}")
        self.assertTrue(response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"])

    def test_multiple_correct_pid(self):
        pids = ["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422",
                "https://b2share.eudat.eu/records/d64361c0a6384760a8a8f32e0dc4a481"]
        response = self.client.get(f"/api/ispid/?pid={','.join(pids)}")
        self.assertTrue(
            response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"] and
            response.json()["https://b2share.eudat.eu/records/d64361c0a6384760a8a8f32e0dc4a481"])

    def test_single_incorrect_pid(self):
        pid = "abcd"
        response = self.client.get(f"/api/sniff/?pid={pid}")
        self.assertFalse(response.json()["abcd"])

    def test_multiple_incorrect_pid(self):
        pids = ["abcd", "efgh"]
        response = self.client.get(f"/api/sniff/?pid={','.join(pids)}")
        self.assertTrue(not response.json()["abcd"] and
                        not response.json()["efgh"])

    def test_mixed_correct_incorrect_pid(self):
        pids = ["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422", "abcd"]
        response = self.client.get(f"/api/sniff/?pid={','.join(pids)}")
        self.assertTrue(
            not response.json()["abcd"]
            and response.json()["https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3422"]
        )
