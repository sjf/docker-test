#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os
import requests
import json
import sys

HTML = """<!DOCTYPE html>
<html>
<head>
  <title>{name}</title>
<!--   <meta http-equiv="refresh" content="5" /> -->
  <meta charset="utf-8">
<style>
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 1.5rem;
    padding: 1rem;
  }}
  pre {{
      white-space: pre-wrap;
      word-wrap: break-word;
      font-size: 1.2rem;
  }}
</style>
</head>
<body>
<h2>{name}</h2>
<strong>Client IP:</strong> {ip} <br>
<strong>Request:</strong> {request} <br>
<strong>Backend response:</strong> {backend_resp}
<p>
<strong>Headers:</strong>

<pre>
{headers}
</pre>
</body>
</html>"""

CONTENT = """
"""

backend_host = os.environ['BACKEND_HOST']
backend_port = os.environ['BACKEND_PORT']
backend = f"http://{backend_host}:{backend_port}/"

def get_backend():
  print(f"  Making request to {backend}")
  response = requests.get(backend)
  res = json.dumps(response.json())
  print(f"  Received {res}")
  return res

class requestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    path = urlparse(self.path).path
    if path == '/favicon.ico':
      self.send_response(404)
      self.end_headers()
      return

    name = sys.argv[0]
    ip = self.client_address[0] # (ip,port)
    request = self.requestline
    headers = "\n".join([ f"{header}: {value}" for header,value in sorted(self.headers.items()) ])

    backend_resp = get_backend()

    print(f"Client IP:{ip}")
    print(f"Request:{request}")
    print(f"Backend:{backend_resp}")
    # print(f"Headers:\n{headers}")
    print("----------------------------\n")

    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()

    html = HTML.format(ip = ip, request = request, headers = headers, backend_resp = backend_resp, name = name)
    # Write content as utf-8 data
    self.wfile.write(bytes(html, "utf8"))
    return

def run():
  server_address = ('0.0.0.0', 8081)
  print('starting server... http://%s:%d' % server_address)
  httpd = HTTPServer(server_address, requestHandler)
  print('running server...')
  httpd.serve_forever()

run()
