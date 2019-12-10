import math
import numpy as np


class BaseLane:
    """
    Base class for lanes used in the car following model

    Attributes
    ----------
    number_of_vehicles : int
        number of vehicles on the lane
    road : Road
        road on which the lane is located
    vehicles : list(Vehicles)
        vehicles on the lane
    initialized : bool
        true if the vehicles are already placed, false if not

    Methods
    -------
    add_vehicle(vehicle)
        add the vehicle to the lane
    initialize_default()
        place the vehicles in a default manner on the lane
    """

    def __init__(self, full_length=100):
        self.full_length = full_length

        self.road = None
        self.vehicles = []
        self.lane_right = None
        self.lane_left = None
        self.initialized = False

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.lane = self

    def get_number_of_vehicles(self):
        return len(self.vehicles)

    def get_speed_difference(self, vehicle1, vehicle2):
        if not vehicle2:
            return math.inf
        if not vehicle1:
            return -math.inf
        return vehicle2.velocity - vehicle1.velocity

    def lane_changes(self):
        vehicles_temp = np.copy(self.vehicles)
        for vehicle in vehicles_temp:
            vehicle.lane_change()

    def remove_vehicle_by_index(self, index):
        del self.vehicles[index]

    def nearby_vehicles(self, vehicle):
        raise NotImplementedError

    def nearby_vehicles_position(self, position):
        raise NotImplementedError

    def initialize_default(self):
        raise NotImplementedError
