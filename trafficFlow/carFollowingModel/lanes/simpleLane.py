from .baseLane import BaseLane


class SimpleLane(BaseLane):
    """
    Class implementing a simple lane

    Inherits from the BaseLane class.

    Attributes
    ----------
    full_length : double
        full length of the lane

    Methods
    -------
    initialize_default()
        override method in class BaseLane and place the vehicles equidistant on the lane
    """
    def __init__(self, full_length=1000.):
        super().__init__(full_length=full_length)

    def initialize_default(self):
        for i, vehicle in enumerate(self.vehicles):
            if self.number_of_vehicles > 1:
                vehicle.predecessor = self.vehicles[(i + 1) % self.number_of_vehicles]
                if i == 0:
                    vehicle.successor = self.vehicles[-1]
                else:
                    vehicle.successor = self.vehicles[i - 1]
            vehicle.position = i * self.full_length / self.number_of_vehicles
            vehicle.velocity = 0.
        self.initialized = True
