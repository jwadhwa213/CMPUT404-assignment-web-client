#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        if data:
            version,code,*rest = data.split(" ")
            return int(code)
        else:
            return None

    def get_headers(self,data):
        if data:
            return data.split('\r\n')[:-1]
        else:
            return None

    def get_body(self, data):
        if data:
            body = data.split('\r\n')[-1]
            return body
        else:
            return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
        
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
                # print(part)
            else:
                # print(buffer.decode('utf-8'))
                done = not part
        # print(buffer.decode('utf-8'))
        return buffer.decode('utf-8')


    def parse_url(self, url):
        '''
        Parse the URL.

        Return: hostname,port and path
        '''

        parseResult = urllib.parse.urlparse(url)

        # hostname
        if parseResult.hostname:
            hostname = parseResult.hostname

        # port
        if parseResult.port:
            port = parseResult.port
        elif parseResult.scheme == "http":
            port = 80
        elif parseResult.scheme == "https":
            port = 443

        # path
        if parseResult.path:
            path = f"{parseResult.path}"
            if parseResult.query:
                path += f"?{parseResult.query}"
        else:
            path = "/"

        return hostname, port, path
 

    def GET(self, url, args=None):
        # 1) get the hostname + port (url_parse)
        hostname, port, path = self.parse_url(url)
        # print(hostname)
        # print(port)

        request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\nAccept: */*\r\nConnection: close\r\n\r\n"
        # print(request)

        # 2) connect
        self.connect(hostname,port)
        

        # 4) send the request
        self.sendall(request)

        # 5) recvall the response
        response = self.recvall(self.socket)
        # response = self.socket.recv(4096).decode('utf-8')

        print(f"-----HERE----  \n {response}")

        self.close()

        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)
    

    def POST(self, url, args=None):

        hostname, port, path = self.parse_url(url)

        request = f"POST {path} HTTP/1.1\r\nHost:{hostname}\r\n"
        request += "Accept: */*\r\n"

        if args:
            args = urllib.parse.urlencode(args)
            request += f"Content-Type: application/x-www-urlencoded\r\n"
            contentLength= len(args.encode('utf-8')) 
            request += f"Content-Length: {contentLength}\r\n"
        else:
            args = ""
            request += "Content-Length: 0\r\n"

        request += "Connection: close\r\n\r\n"
        request += args

        self.connect(hostname,port)

        self.sendall(request)

        response = self.recvall(self.socket)
        # response = self.socket.recv(4096).decode('utf-8')
        self.close()

        code = self.get_code(response)
        body = self.get_body(response)
    
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
