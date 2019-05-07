class ParkingLot:
    """
    Represents projected 3 story parking structure with 30 places
    """
    capacity = 0
    lots = [] # False - place is available, True - taken

    def __init__(self):
        self.capacity = 30
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
    
class Encoder:
    # Skeleton
    elevator_engine1 = int()
    elevator_engine2 = int()
    rotation_engine1 = int()
    rotation_engine2 = int()
    picker_engine    = int()
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
        return []

    def rotate_elevator(self, degree):
        """
        Rotates elevator by degree
        positive degree is clockwise, negative is couner-clockwise
        Returns
        -------
        command_list: `[str]`
        """
        return []
    
    def place_car(self):
        """
        Places car from elevator to place
        Returns
        -------
        command_list: `[str]`
        """
        
        return []
    
    def take_car(self):
        """
        Take car from place on elevator
        Returns
        -------
        command_list: `[str]`
        """
        return []

    def mm_to_rotation_time(self):
        """
        Transforms distance values to engine rotation_time
        Returns
        -------
        rotation_time: 'int'
        """
