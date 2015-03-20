"""
Unit tests for stub HTTP server base class.
"""
import unittest
import requests
import json
from ..redirector import FirebaseRedirectService


class FirebaseServiceTest(unittest.TestCase):

    def setUp(self):
        self.server = FirebaseRedirectService()
        self.addCleanup(self.server.shutdown)
        self.url = "http://127.0.0.1:{0}/foo".format(self.server.port)

    def test_require_fb_path_param(self):
        response = requests.post(self.url)
        self.assertEqual(response.status_code, 400)
        response = requests.post(self.url, data={"fb_path": 2})
        self.assertEqual(response.status_code, 200)
