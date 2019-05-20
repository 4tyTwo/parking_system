from serial import Serial

class ParkingLot:
    """
    Represents projected 3 story parking structure with 23 places
    """
    commander = None
    commanderBlueooth = None
    capacity = 0
    lots = [] # False - place is available, True - taken
    encoder = None

    def __init__(self, device1, device2):
        self.capacity = 23
        self.commander = Commander(device1, 9600, 5)  # elevator
        self.commanderBlueooth = Commander(device2, 9600, 5)   # platform
        self.encoder = Encoder()
        self.lots = [False] * self.capacity

    def store(self):
        """
        Stores vehicle inside the lot.
        Returns
        -------
        position: `int`, if executed correctly, raises `exception` if there are no free spaces
        """
        if self.places_available() == 0:
            raise Exception('No places available')
        position = self.__pick_place()
        self.__do_strore(position)
        self.commander.write_commands(self.encoder.elevator_vertical(self.__floor(position)))
        self.commanderBlueooth.write(self.encoder.rotate_elevator(90) + self.encoder.place_car())
        return position
        
    def take(self, position):
        """
        Takes vehicle stored at position
        Parametres
        ----------
        position: `int`
        Returns
        -------
        Nothing if executed correctly, raises `exception` if no vehicle stored at position or poistion exceeds capacity
        """
        if position < self.capacity:
            if self.__is_taken(position):
                # TODO add validation (operation UUID perhaps)
                self.__do_take(position)
                return
        raise Exception('Incorrect position')


    def places_available(self):
        """
        Returns
        -------
        `Int` number of available spaces
        """
        return self.lots.count(False)
    
    def __pick_place(self):
        return self.lots.index(False) # TODO balancing

    def __do_strore(self, position):
        self.lots[position] = True
    
    def __do_take(self, position):
        self.lots[position] = False

    def __is_taken(self, position):
        return self.lots[position]
    
    def __floor(self, position):
        return int(position / 3) + 1

class Encoder:
    # Skeleton
    full_rotation = 2076 # steps
    step_per_degree = full_rotation / 360

    """
    Translates abstract store/take commands to concrete arduino engines commands
    """
    def elevator_vertical(self, value):
        """
        Moves elevator verticaly by value mm
        Returns
        -------
        command_list: `[str]`
        """
        return [str(value) * self.full_rotation]

    def rotate_elevator(self, degree):
        """
        Rotates elevator by degree
        positive degree is clockwise, negative is couner-clockwise
        Returns
        -------
        command_list: `[str]`
        """
        return ['rot' + str(self.step_per_degree * degree)]
    
    def rotate_position(self, positions):
        return ['rot ' + str(positions)]

    def place_car(self):
        """
        Places car from elevator to place
        Returns
        -------
        command_list: `[str]`
        """
        
        return ['push 1300', 'push -1300']
    
    def push_car(self):
        """
        Push car from elevator
        Returns
        -------
        command_list: `[str]`
        """
        return ['push 1300']
    
    def pull_car(self):
        """
        Pull car on elevator
        Returns
        -------
        command_list: `[str]`
        """
        return ['push -1300']

class Commander:
    """
    Commander sends commands to given serial device
    """

    device = None
    __buffer_size = 64 # Arduino Uno's default buffer size

    def __init__(self, device_path, bitrate = 9600, timeout = 5):
        self.device = Serial(device_path, bitrate, timeout=timeout)

    def write(self, message):
        if len(message) <= self.__buffer_size:
            msg = bytes(message, 'UTF-8')
            self.device.timeout = 5
            self.device.write(msg)
            # waiting for OK from arduino
            # OK means that board accepted command
            outp = self.device.readline().decode('UTF-8')
            print("Response:", outp)
            self.device.close()
            if self.device.readline().decode('UTF-8') == 'OK\r\n':
                self.device.timeout = 30
                if self.device.readline().decode('UTF-8') == 'DONE\r\n':
                    return
                else:
                    raise Exception('No Done')
            else:
                raise Exception('Arduino didn\'t respond in time')
        else:
            raise Exception('Buffer limit exceeded')

    def write_commands(self, message_list):
        for message in message_list:
            self.write(message)
