import requests
import http.client
import uuid

# System MUST be blocked while executing request

class Reader:
    # Prototype of CLI parking system client
    client = None
    def __init__(self, client):
        self.client = client
    """Reads and parses standart input, invokes parkingLot commands
    
    Possible commands: take n, store, get places
    
    """
    def read(self):
        return self.__format(self.__do_read())

    def __do_read(self):
        input_string = input('Enter command: ')
        if input_string == 'store':
            # curl --request POST \
            # --url http://127.0.0.1:4242/ \
            # --header 'content-type: application/json' \
            # --header 'idempotency-key: 8254cde7-9b8e-464f-9672-3439d39dc702' \
            # --data '{\n	"action": "store"\n}'
            return self.client.store()
        elif input_string == 'get places':
            return self.client.get_places()
        else:
            try:
                splited = input_string.split(' ')
                if splited[0] == 'take':
                    position = int(splited[1])
                    return self.client.take(position)
                else:
                    raise Exception('Unknown action')
            except:
                return None

    def __format(self, result):
        if result == None:
            return 'An error occured, try again'
        if 'Error' in result.headers:
            return 'Error: ' + result.headers['Error']
        if result.status_code == 202:
            return 'Accepted'
        elif result.status_code == 200:
            return 'Parking lot has ' + str(result.headers['Places']) + ' free places'

class ParkingClient:
    def __init__(self, url, port):
        self.url = url + ':' + str(port)
        self.__generate_idempotency_key()

    def __generate_idempotency_key(self):
        self.idempotency_key = str(uuid.uuid4())

    def __do_request(self, method, data):
        resp = requests.request(method, self.url, json=data, headers={
            'Idempotency-Key': self.idempotency_key})
        self.__generate_idempotency_key()
        return resp

    def store(self):
        try:
            data = {'action': 'store'}
            return self.__do_request('post', data)
        except:
            print('Store returned error')
            return None

    def get_places(self):
        try:
            return self.__do_request('get', {})
        except:
            print('Get places returned error')
            return None

    def take(self, posititon):
        try:
            data = {
                'action': 'take',
                'position': posititon
            }
            return self.__do_request('post', data)
        except:
            print('Take returned error')
            return None
        

# Example usage
try:
    client = ParkingClient('http://127.0.0.1', 4242)
    reader = Reader(client)
    while True:
        print(reader.read())
except KeyboardInterrupt:
	pass
