from http.server import BaseHTTPRequestHandler, HTTPServer
from uuid import UUID
from queue import Queue
import random
import json

class MyServer(BaseHTTPRequestHandler):
    used_keys = []
    allowed_commands = ['take', 'store']
    can_continue = True
    validation_rules = {}

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.validation_rules = {
            'Content-type': lambda header: header == 'application/json',
            'Idempotency-Key': lambda header: self.__validate_idempotency_key(header)
        }

    def __response_error(self, code, error_message):
        self.send_response(code)
        self.send_header('Error', error_message)
        self.end_headers()

    def __response(self, code, headers = {}):
        self.send_response(code)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()

    def do_GET(self):
        print('GET')
        self.__validate_headers(['Idempotency-Key'])
        if not self.can_continue:
            return
        self.__response(200, {
            'Free places': self.__get_free_spaces()
        })

    def do_HEAD(self):
        print('HEAD')
        self.__response(405)
        
    def do_POST(self):
        self.__validate_headers(
            ['Content-type', 'Content-Length', 'Idempotency-Key'])
        if not self.can_continue:
            return
        self.content = self.get_content()
        if not self.can_continue:
            return
        print('POST:', self.content)
        if not self.can_continue:
            return
        self.__validate_command()
        if not self.can_continue:
            return
        self.process_command()
    
    def get_content(self):
        content_length = int(self.headers['Content-Length'])
        try:
            content = json.loads(self.rfile.read(content_length))
        except:
            self.__response_error(400, 'Incorrect JSON')
        return content

    def __validate_command(self):
        command = self.content
        if 'action' in command:
            if command['action'] == 'take':
                if not 'position' in command:
                    self.__response_error(400, 'No position specified')
                    self.can_continue = False
                elif command['position'] >= 30 or command['position'] < 0:  # TODO get value from parking lot
                        self.__response_error(400, 'Incorrect position')
                        self.can_continue =  False
            elif command['action'] != 'store':
                self.__response_error(400, 'Unrecognized action')
        else:
            self.__response_error(400, 'Missing action')
            self.can_continue = False

    def process_command(self):
        self.send_response(202)
        self.end_headers()

    def __validate_headers(self, headers):
        for header in headers:
            if not self.can_continue:
                return
            self.__validate_header_existance(header)
            if not self.can_continue:
                    return
            self.__validate_header_value(
                header,
                self.validation_rules.get(header, lambda x : True)
            )
        if not self.can_continue:
            return
    
    def __validate_header_existance(self, headerName):
        if not headerName in self.headers:
            self.__response_error(400, 'Missing ' + headerName + ' header')
            self.can_continue = False

    def __validate_header_value(self, headerName, fun):
        if fun(self.headers[headerName]) == False:
            self.__response_error(400, 'Incorrect value of ' +
                            headerName + ' header')
            self.can_continue = False

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

    def __get_free_spaces(self):
        # placeholder TODO get value from parking lot
        return random.randint(0, 30)

hostName = ''
hostPort = 4242

myServer = HTTPServer((hostName, hostPort), MyServer)
print('Server Starts - %s:%s' % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
