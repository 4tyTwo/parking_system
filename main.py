import requests
import http.client
import uuid

# System MUST be blocked while executing request

class Reader:
    # Prototype of CLI parking system client
    """Reads and parses standart input, invokes parkingLot commands
    
    Possible commands: take n, store
    
    """
    def read(self):
        input_string = input('Enter command')
        if input_string == 'store':
            # curl --request POST \
            # --url http://127.0.0.1:4242/ \
            # --header 'content-type: application/json' \
            # --header 'idempotency-key: 8254cde7-9b8e-464f-9672-3439d39dc702' \
            # --data '{\n	"action": "store"\n}'
            pass
        elif input_string == 'take n':
            # See above
            pass

class ParkingClient:

    def __init__(self, url, port):
        self.url = url + ':' + str(port)
        self.__generate_idempotency_key()

    def __generate_idempotency_key(self):
        self.idempotency_key = str(uuid.uuid4())

    def __do_request(self, data):
        resp = requests.post(self.url, json=data, headers={
            'Idempotency-Key': self.idempotency_key})
        self.__generate_idempotency_key()
        return resp

    def store(self):
        try:
            data = {'action': 'store'}
            resp = self.__do_request(data)
            print('Server rerturned:', resp.status_code) # TODO remove
            print(resp.headers) # TODO remove
            return resp
        except:
            print('Store returned error')
            return None

    def take(self, posititon):
        try:
            data = {
                'action': 'take',
                'position': posititon
            }
            resp = self.__do_request(data)
            print('Server rerturned:', resp.status_code)  # TODO remove
            print(resp.headers)  # TODO remove
            return resp
        except:
            print('Take returned error')
            return None
        

# Example usage
client = ParkingClient('http://127.0.0.1', 4242)
client.store()  # 202
client.take(5)  # 202
client.take(40) # 400, Incorrect position
client.take(-1) # 400, Incorrect position
