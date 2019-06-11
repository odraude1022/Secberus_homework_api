#!/usr/bin/env python3

import json
import time
import uuid
import random
from typing import Optional, Dict, Any
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 5000

class SimpleAPI(BaseHTTPRequestHandler):

    protocol_version: str = 'HTTP/1.1'

    no_auth_response: Dict[str, Any] = {
        'body': None,
        'status': 401,
        'headers': {
            'WWW-Authenticate': 'Bearer realm="{}"'.format(HOST_NAME)
        }
    }

    tokens: Dict[str, int] = {}

    def do_POST(self) -> None:
        paths = ['/api/login']

        if self.path in paths:
            try:
                content_length = int(self.headers['Content-Length'])
                payload = self.rfile.read(content_length)
                creds = json.loads(payload.decode('UTF-8'))
                if not creds['username'] == 'guest' or not creds['password'] == 'guest':
                    raise Exception

                token = str(uuid.uuid4())
                self.tokens[token] = 0
                self.respond(body=json.dumps({'access_token': token}))

            except Exception:
                self.respond(**self.no_auth_response)
        else:
            self.respond(status=404)

    def do_GET(self) -> None:
        paths = {
            '/api/secret1': 'The first door, unlocked.',
            '/api/secret2': 'The second answer.',
            '/api/secret3': 'The final test.',
        }

        if self.path in paths:
            if 'Authorization' not in self.headers or not self.check_login():
                self.respond(**self.no_auth_response)
            else:
                self.respond(body=json.dumps({'answer': paths[self.path]}))
        else:
            self.respond(status=404)

    def check_login(self) -> bool:
        """ Check the Authorization header """
        try:
            r = random.randint(1,3)
            scheme, token = self.headers['Authorization'].split(' ')
            if scheme != 'Bearer' or token not in self.tokens:
                return False
            if self.tokens[token] >= r:
                return False
            self.tokens[token] += 1
            return True
        except Exception:
            pass
        return False

    def respond(self,
                body: Optional[str] = None,
                status: int = 200,
                headers: Optional[Dict[str, str]] = None) -> None:

        body_bytes = None
        content_length = 0

        self.send_response(status)
        if headers:
            for k,v in headers.items():
                self.send_header(k, v)
        if body:
            self.send_header('Content-type', 'application/json')
            body_bytes = bytes(body, 'UTF-8')
            content_length = len(body_bytes)
        self.send_header('Content-Length', content_length)
        self.end_headers()
        self.flush_headers()
        if body_bytes:
            self.wfile.write(body_bytes)

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), SimpleAPI)
    print(time.asctime(), 'Server Start - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stop - %s:%s' % (HOST_NAME, PORT_NUMBER))
