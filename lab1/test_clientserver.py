"""
Simple client server unit test
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test


    # TESTS

    def test_srv_get(self):
        """Test simple GET"""
        msg = self.client.GET("Hofmann")
        self.assertEqual(msg, 'Hofmann: 15643\n')

    def test_srv_getnotfound(self):
        """Test with unknown name"""
        msg = self.client.GET("Schmidt")
        self.assertEqual(msg, "Schmidt not found\n")

    def test_srv_getall(self):
        """Test simple GETALL"""
        msg = self.client.GETALL()
        self.assertEqual(msg, "Korn: 13245\nWeber: 54321\nHofmann: 15643\nBjörn: 645646")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
