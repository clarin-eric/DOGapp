from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
import unittest

from dogapi.utils import parse_queryparam


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
