"""
Unit tests for stub HTTP server base class.
"""
import unittest
import requests
import json
from ..http import StubHttpService, StubHttpRequestHandler, require_params

class StubHttpServiceTest(unittest.TestCase):

    def setUp(self):
        self.server = StubHttpService()
        self.addCleanup(self.server.shutdown)
        self.url = "http://127.0.0.1:{0}/set_config".format(self.server.port)

    def test_bad_json(self):
        response = requests.put(self.url, data="{,}")
        self.assertEqual(response.status_code, 400)

    def test_no_post_data(self):
        response = requests.put(self.url, data={})
        self.assertEqual(response.status_code, 200)

    def test_unicode_non_json(self):
        # Send unicode without json-encoding it
        response = requests.put(self.url, data={'test_unicode': u'\u2603 the snowman'})
        self.assertEqual(response.status_code, 400)

    def test_unknown_path(self):
        response = requests.put(
            "http://127.0.0.1:{0}/invalid_url".format(self.server.port),
            data="{}"
        )
        self.assertEqual(response.status_code, 404)


class RequireRequestHandler(StubHttpRequestHandler):
    @require_params('GET', 'test_param')
    def do_GET(self):
        self.send_response(200)

    @require_params('POST', 'test_param')
    def do_POST(self):
        self.send_response(200)


class RequireHttpService(StubHttpService):
    HANDLER_CLASS = RequireRequestHandler

class RequireParamTest(unittest.TestCase):
    """
    Test the decorator for requiring parameters.
    """

    def setUp(self):
        self.server = RequireHttpService()
        self.addCleanup(self.server.shutdown)
        self.url = "http://127.0.0.1:{port}".format(port=self.server.port)

    def test_require_get_param(self):

        # Expect success when we provide the required param
        response = requests.get(self.url, params={"test_param": 2})
        self.assertEqual(response.status_code, 200)

        # Expect failure when we do not proivde the param
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 400)

        # Expect failure when we provide an empty param
        response = requests.get(self.url + "?test_param=")
        self.assertEqual(response.status_code, 400)

    def test_require_post_param(self):

        # Expect success when we provide the required param
        response = requests.post(self.url, data={"test_param": 2})
        self.assertEqual(response.status_code, 200)

        # Expect failure when we do not proivde the param
        response = requests.post(self.url)
        self.assertEqual(response.status_code, 400)

        # Expect failure when we provide an empty param
        response = requests.post(self.url, data={"test_param": None})
        self.assertEqual(response.status_code, 400)
