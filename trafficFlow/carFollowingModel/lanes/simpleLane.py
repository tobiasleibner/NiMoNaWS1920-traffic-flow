import math

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

    def __init__(self, full_length=100.):
        super().__init__(full_length)

    def nearby_vehicles(self, vehicle):
        num_vehicles = self.get_number_of_vehicles()
        if num_vehicles <= 1:
            return None, None
        index = self.vehicles.index(vehicle)
        return self.vehicles[(index-1) % num_vehicles], self.vehicles[(index+1) % num_vehicles]

    def nearby_vehicles_position(self, position):
        num_vehicles = len(self.vehicles)
        for i in range(len(self.vehicles)):
            if self.road.between(self.vehicles[i].position, position, self.vehicles[(i + 1) % num_vehicles].position):
                return self.vehicles[i], self.vehicles[(i + 1) % num_vehicles], i, (i + 1) % num_vehicles
        return None, None, None, None

    def initialize_default(self):
        num_vehicles = self.get_number_of_vehicles()
        for i, vehicle in enumerate(self.vehicles):
            if num_vehicles > 1:
                vehicle.predecessor = self.vehicles[(i + 1) % num_vehicles]
                if i == 0:
                    vehicle.successor = self.vehicles[-1]
                else:
                    vehicle.successor = self.vehicles[i - 1]
            vehicle.position = i * self.full_length / num_vehicles
            vehicle.velocity = 0.
        self.initialized = True
