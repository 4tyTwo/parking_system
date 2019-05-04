from http.server import BaseHTTPRequestHandler, HTTPServer
from uuid import UUID
from queue import Queue
import random
import json

class MyServer(BaseHTTPRequestHandler):
    used_keys = []
    allowed_commands = ['take', 'store']
    def _set_headers(self, code, headers = {}):
        self.send_response(code)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()

    def do_GET(self):
        print("GET")
        self._set_headers(405)

    def do_HEAD(self):
        print("HEAD")
        self._set_headers(405)
        
    def do_POST(self):
        self.__validate_headers()
        self.content = self.get_content()
        print('POST:', self.content)
        self.__validate_command()
        self.process_command()
    
    def get_content(self):
        content_length = int(self.headers['Content-Length'])
        try:
            content = self.rfile.read(content_length)
        except:
            self.send_error(400, 'Incorrect JSON')
        return content

    def __validate_command(self):
        command = self.content
        if "action" in command:
            if command['action'] == 'take':
                if not 'position' in command:
                    self.send_error(400, 'No position specified')
                elif command["position"] >= 30 or command["position"] < 0:  # TODO get value from parking lot
                        self.send_error(400, "Incorrect postion")
        else:
            self.send_error(400, 'Missing action')

    def process_command(self):
        self.send_response(202)

    def __validate_headers(self):
        map(self.__validate_header_existance, [
            'Content-type',
            'Idempotency-Key',
            'Content-Length'
        ])
        self.__validate_header_value(
            'Content-type',
            lambda header: header == 'application/json'
        )
        self.__validate_header_value(
            'Idempotency-Key',
            lambda header: self.__validate_idempotency_key(header)
        )
    
    def __validate_header_existance(self, headerName):
        if not headerName in self.headers:
            self.send_error(400, "Missing" + headerName + "header")

    def __validate_header_value(self, headerName, fun):
        if fun(self.headers[headerName]) == False:
            self.send_error(400, "Incorrect value of " +
                            headerName + " header")

    def __validate_idempotency_key(self, key):
        return key not in self.used_keys and self.__is_valid_uuid(key)

    def __is_valid_uuid(self, uuid_to_test, version=4):
        """
        Check if uuid_to_test is a valid UUID.

        Parameters
        ----------
        uuid_to_test : str
        version : {1, 2, 3, 4}

        Returns
        -------
        `True` if uuid_to_test is a valid UUID, otherwise `False`.
        """
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except:
            return False

        return str(uuid_obj) == uuid_to_test


hostName = ""
hostPort = 4242

myServer = HTTPServer((hostName, hostPort), MyServer)
print("Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
