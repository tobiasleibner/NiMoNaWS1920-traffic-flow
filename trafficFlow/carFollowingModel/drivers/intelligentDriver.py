import numpy as np

from .baseDriver import BaseDriver


class IntelligentDriver(BaseDriver):
    """
    Class to model the intelligent driver with the intelligent way of changing the acceleration

    Inherits from the BaseDriver class.

    Attributes
    ----------
    s_0 : double
        minimum distance to the predecessor
    v_0 : double
        desired speed of the driver
    delta : double
        acceleration exponent
    T : double
        follow time
    a : double
        acceleration of the vehicle
    b : double
        delay of the driver

    Methods
    -------
    get_distance_to_predecessor()
        compute distance to the predecessor (using the get_distance method of the road)
    get_speed_difference_to_predecessor()
        compute difference in the speed of the predecessor and oneself
    get_desired_distance()
        compute the desired distance using the speed difference to the predecessor
        according to the intelligent driver model
    get_desired_acceleration()
        override method in class BaseDriver to calculate the desired acceleration
        according to the intelligent driver model
    """

    def __init__(self, s_0, v_0, delta, T, a, b, length=4., lane_change_safety_distance=50., label=""):
        super().__init__(length=length, lane_change_safety_distance=lane_change_safety_distance, label=label)
        self.s_0 = s_0
        self.v_0 = v_0
        self.delta = delta
        self.T = T
        self.a = a
        self.b = b

    def get_desired_distance(self):
        predecessor, successor = self.lane.nearby_vehicles(self)
        if predecessor:
            return self.s_0 + max(0., self.velocity * self.T
                                  + (self.velocity * self.lane.get_speed_difference(predecessor, self))
                                  / (2. * np.sqrt(self.a * self.b)))
        else:
            return 0.

    def get_desired_acceleration(self):
        predecessor, successor = self.lane.nearby_vehicles(self)
        if predecessor:
            return self.a * (1. - np.power(self.velocity / self.v_0, self.delta)
                             - np.power(self.get_desired_distance()
                                        / self.lane.road.get_distance(predecessor, self), 2))
        else:
            return self.a * (1. - np.power(self.velocity / self.v_0, self.delta))

    def lane_change(self):
        changed = False

        if self.lane.lane_right:
            predecessor_right, successor_right, _, _ = self.lane.lane_right.nearby_vehicles_position(self.position)
            if self.lane.road.get_distance(predecessor_right, self) >= self.lane_change_safety_distance \
                    and self.lane.road.get_distance(self, successor_right) >= self.lane_change_safety_distance:
                self.change_to_right_lane()
                changed = True

        if not changed and self.lane.lane_left:
            predecessor_left, successor_left, _, _ = self.lane.lane_left.nearby_vehicles_position(self.position)
            predecessor, successor = self.lane.nearby_vehicles(self)
            if predecessor \
                    and self.lane.road.get_distance(predecessor_left, self) >= self.lane_change_safety_distance \
                    and self.lane.road.get_distance(self, successor_left) >= self.lane_change_safety_distance \
                    and predecessor.velocity < self.v_0 \
                    and (self.lane.road.get_distance(predecessor, self) <= self.lane_change_safety_distance):# or self.get_desired_acceleration()<0.):
                self.change_to_left_lane()
                changed = True
        ####################################################

    def change_to_right_lane(self):
        ####################################################
        _, _, predecessor_right_index, successor_right_index = self.lane.lane_right.nearby_vehicles_position(self.position)
        if successor_right_index is None:
            successor_right_index = 0
        self.lane.vehicles.remove(self)
        self.lane.lane_right.vehicles.insert(successor_right_index, self)
        self.lane = self.lane.lane_right

    def change_to_left_lane(self):
        ####################################################
        _, _, predecessor_left_index, successor_left_index = self.lane.lane_left.nearby_vehicles_position(self.position)
        if successor_left_index is None:
            successor_left_index = 0
        self.lane.vehicles.remove(self)
        self.lane.lane_left.vehicles.insert(successor_left_index, self)
        self.lane = self.lane.lane_left
