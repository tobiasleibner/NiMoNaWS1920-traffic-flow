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

    def __init__(self, s_0, v_0, delta, T, a, b, length=4., label=""):
        super().__init__(length=length, label=label)
        self.s_0 = s_0
        self.v_0 = v_0
        self.delta = delta
        self.T = T
        self.a = a
        self.b = b

    def get_desired_distance(self):
        successor, predecessor = self.lane.nearby_vehicles(self)
        if predecessor:
            return self.s_0 + max(0., self.velocity * self.T
                                  + (self.velocity * self.lane.get_speed_difference(predecessor, self))
                                  / (2. * np.sqrt(self.a * self.b)))
        else:
            return 0.

    def get_desired_acceleration(self):
        successor, predecessor = self.lane.nearby_vehicles(self)
        return self.a * (1. - np.power(self.velocity / self.v_0, self.delta)
                         - np.power(self.get_desired_distance()
                                    / self.lane.get_distance(predecessor, self), 2))
