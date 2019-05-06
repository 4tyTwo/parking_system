class ParkingLot:
    """
    Represents projected 3 story parking structure with 30 places
    """
    capacity = 30
    lots = [False] * capacity # False - place is available, True - taken

    def store(self):
        """
        Stores vehicle inside the lot.
        Returns
        -------
        Nothing if executed correctly, raises `exception` if there are no free spaces
        """
        if self.places_avaiable() == 0:
            raise Exception('No places available')
        
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


    def places_avaiable(self):
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
    
