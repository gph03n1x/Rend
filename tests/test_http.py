#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import unittest
import requests
from random import randint
from core.index_struct import SpatialIndex
from core.http_handler import make_http_server
from plugins.quad_tree import QuadTreeIndex


class TestHTTPServer(unittest.TestCase):
    def setUp(self):
        self.points = list(set([
            (randint(-500, 500), randint(-500, 500),) for num in range(100000)
        ]))
        self.spatial_index = SpatialIndex()
        self.spatial_index.set(QuadTreeIndex)
        self.spatial_index.index.add_points(self.points)
        self.httpd = make_http_server(self.spatial_index, port=8888)
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def test_request(self):
        r = requests.get('http://127.0.0.1:8888/nearest/x=10/y=50/k=30')
        self.assertEqual(r.status_code, 200)

    def tearDown(self):
        self.httpd.shutdown()


suite = unittest.TestLoader().loadTestsFromTestCase(TestHTTPServer)
unittest.TextTestRunner(verbosity=2).run(suite)
