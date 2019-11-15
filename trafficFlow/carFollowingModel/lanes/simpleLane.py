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
        if index == 0:
            return self.vehicles[-1], self.vehicles[1]
        if index == num_vehicles-1:
            return self.vehicles[-2], self.vehicles[0]
        return self.vehicles[index-1], self.vehicles[index+1]

    def get_distance(self, vehicle1, vehicle2):
        if not vehicle1:
            return self.full_length  # math.inf
        if not vehicle2:
            return self.full_length  # math.inf
        if vehicle1.position >= vehicle2.position:
            return vehicle1.position - vehicle2.position
        else:
            return vehicle1.position - vehicle2.position + vehicle1.lane.full_length

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
