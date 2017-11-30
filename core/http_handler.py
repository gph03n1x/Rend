#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer


class SpatialHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(SpatialHandler, self).__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path.endswith(".ico"):
            with open("images/icon.png", "rb") as ifp:
                self.wfile.write(ifp.read())
        else:

            action, params = self.path[1:].split("/", 1)
            d = {}
            for param in params.split("/"):
                key, value = param.split("=")
                d[key] = int(value)

            time_, results = self.server.spatial_index.action(action, d)
            self.wfile.write(str(results).encode())


def run(spatial_index, server_class=HTTPServer, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, SpatialHandler)
    httpd.spatial_index = spatial_index
    print('Starting httpd...')
    httpd.serve_forever()
