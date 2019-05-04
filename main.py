from serial import Serial
from queue import Queue

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

        

# An example of serial communication, that will be used by the server
ser = Serial('/dev/tty.usbmodem14201', 9600, timeout=5)
while True:
    message = bytes(input("Print message: "), 'UTF-8')
    print("Sending message:", message)
    print("Sent", ser.write(message), "bytes of data")
    print("received message:", ser.readline().decode('UTF-8'), end='')
