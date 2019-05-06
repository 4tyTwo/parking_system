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
    
