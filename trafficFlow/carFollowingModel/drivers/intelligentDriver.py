import numpy as np


class IntelligentDriver:
    def __init__(self, s_0, v_0, delta, T, a, b):
        self.s_0 = s_0
        self.v_0 = v_0
        self.delta = delta
        self.T = T
        self.a = a
        self.b = b

        self.road = None
        self.velocity = 0.
        self.position = 0.
        self.predecessor = None
        self.successor = None

    def get_distance(self):
        return self.road.get_distance(self.predecessor.position, self.position)

    def get_speed_difference(self):
        return self.predecessor.velocity - self.velocity

    def get_desired_distance(self):
        return self.s_0 + max(0., self.velocity*self.T+(self.velocity*self.get_speed_difference())/(2.*np.sqrt(self.a*self.b)))

    def get_desired_acceleration(self):
        return self.a * (1. - np.power(self.velocity/self.v_0, self.delta)
                            - np.power(self.get_desired_distance()/self.get_distance(), 2))
