from http.server import BaseHTTPRequestHandler, HTTPServer
from uuid import UUID
from queue import Queue
import random
import json
from parkingLot import ParkingLot, Commander

class ParkingServer(HTTPServer):
    parking = None
    used_keys = []
    validation_rules = {}
    def __init__(self, Host, handlerClass, device1, device2):
        HTTPServer.__init__(self, Host, handlerClass)
        self.parking = ParkingLot(device1, device2)
        self.validation_rules = {
            'Content-type': lambda header: header == 'application/json',
            'Idempotency-Key': lambda header: self.__validate_idempotency_key(header)
        }

    def __validate_idempotency_key(self, key):
        valid = key not in self.used_keys and self.__is_valid_uuid(key)
        if valid == True:
            self.used_keys.append(key)
        return valid

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

class MyServer(BaseHTTPRequestHandler):
    allowed_commands = ['take', 'store']
    content = None
    method = ''

    def __create_error(self, error_msg):
        return {'Error': error_msg}

    def __response(self, code, headers = {}):
        self.send_response(code)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()

    def do_GET(self):
        self.method = 'GET'
        code, headers = self.__validate_headers(['Idempotency-Key'])
        self.__response(code, headers)

    def do_HEAD(self):
        self.__response(405)
        
    def do_POST(self):
        self.method = 'POST'
        code, headers = self.__validate_headers(
            ['Content-type', 'Content-Length', 'Idempotency-Key'])
        self.__response(code, headers)
        

    def __validate_headers(self, headers):
        for header in headers:
            if self.__header_exists(header) == False:
                return 400, self.__create_error('Missing ' + header + ' header')
            if self.__header_correct(
                header,
                self.server.validation_rules.get(header, lambda x: True)
            ) == False:
                return 400, self.__create_error('Incorrect value of ' +
                    header + ' header')
        return self.__process_request()
    
    def __process_request(self):
        if self.method == 'POST':
            return self.__process_POST()
        elif self.method == 'GET':
            return self.__process_GET()
    
    def __process_POST(self):
        return self.get_content()

    def __process_GET(self):
        return 200, {'Free places': self.__get_free_spaces()}

    def get_content(self):
        content_length = int(self.headers['Content-Length'])
        try:
            self.content = json.loads(self.rfile.read(content_length))
            return self.__validate_command()
        except:
            return 400, self.__create_error('Incorrect JSON')

    def __validate_command(self):
        command = self.content
        if 'action' in command:
            if command['action'] == 'take':
                if 'position' in command:
                    return self.process_command()
                else:
                    return 400, self.__create_error('No position specified')
            elif command['action'] != 'store':
                return 400, self.__create_error('Unrecognized action')
            else:
                return self.process_command()
        else:
            return 400, self.__create_error('Missing action')

    def process_command(self):
        if self.content['action'] == 'store':
            try:
                position = self.server.parking.store()
                return 202, {'Position': position}
            except:
                return 400, self.__create_error('Parking lot is full')
        elif self.content['action'] == 'take':
            position = int(self.content['position'])
            try:
                self.server.parking.take(position)
                return 202, {}
            except:
                return 400, self.__create_error('No car at position')

#
## utils
#

    def __header_exists(self, headerName):
        return headerName in self.headers

    def __validate_header_existance(self, headerName):
        return headerName in self.headers

    def __header_correct(self, headerName, correctness_fun):
        return correctness_fun(self.headers[headerName])

    def __validate_header_value(self, headerName, fun):
        return fun(self.headers[headerName])

    def __get_free_spaces(self):
        return self.server.parking.places_available()

hostName = ''
hostPort = 4242

myServer = ParkingServer((hostName, hostPort),
                         MyServer, '/dev/tty.usbmodem14101', '/ dev/tty.HC-06-SPPDev')
print('Server Starts - %s:%s' % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
