#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
from core.utils import get_allowed_actions


class SpatialHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(SpatialHandler, self).__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        if self.path.endswith("/"):
            self.path = self.path[:-1]

        if self.path.endswith(".ico"):
            with open("images/icon.png", "rb") as ifp:
                self.wfile.write(ifp.read())
        else:
            action, params = self.path[1:].split("/", 1)
            d = {}
            for param in params.split("/"):
                key, value = param.split("=")
                d[key] = int(value)

            if action in self.server.allowed_actions:
                results = self.server.spatial_index.action(action, d)
                self.wfile.write(str(results).encode())


def make_http_server(spatial_index, port, server_class=HTTPServer):
    server_address = ('', port)
    httpd = server_class(server_address, SpatialHandler)
    httpd.spatial_index = spatial_index
    httpd.allowed_actions = get_allowed_actions(spatial_index.index.ACTIONS)
    return httpd
