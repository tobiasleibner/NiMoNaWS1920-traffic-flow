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

    def __init__(self, s_0, v_0, delta, T, a, b, length=4., lane_change_safety_distance=100., label=""):
        super().__init__(length=length, lane_change_safety_distance=lane_change_safety_distance, label=label)
        self.s_0 = s_0
        self.v_0 = v_0
        self.delta = delta
        self.T = T
        self.a = a
        self.b = b

    def get_desired_distance(self):
        return self.s_0 + max(0., self.velocity*self.T
                            + (self.velocity*self.get_speed_difference_to_predecessor()) / (2.*np.sqrt(self.a*self.b)))

    def get_desired_acceleration(self):
        return self.a * (1. - np.power(self.velocity/self.v_0, self.delta)
                            - np.power(self.get_desired_distance()/self.get_distance_to_predecessor(), 2))
