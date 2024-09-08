#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os
import json
import sys

class requestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/json')
    self.end_headers()

    name = sys.argv[0]
    version = '0.1'
    path = urlparse(self.path).path
    ip = self.client_address[0] # (ip,port)

    content = {'server': name, 'version': version, 'client-ip': ip, 'path': path}
    response = json.dumps(content)

    # Write content as utf-8 data
    self.wfile.write(bytes(response, "utf8"))
    return

def run():
  port = 7777
  if 'PORT' in os.environ:
    port = int(os.getenv['PORT'])

  server_address = ('0.0.0.0', port)

  print('starting backend... http://%s:%d' % server_address)
  httpd = HTTPServer(server_address, requestHandler)
  print('running server...')
  httpd.serve_forever()

run()
