import numpy as np


class VehicleIntelligentDriver:
    def __init__(self, s_0, v_0, delta, T, a, b):
        self.s_0 = s_0
        self.v_0 = v_0
        self.delta = delta
        self.T = T
        self.a = a
        self.b = b

    def get_desired_distance(self, v, dv):
        return self.s_0 + max(0., v*self.T+(v*dv)/(2.*np.sqrt(self.a*self.b)))


class IntelligentDriverModel:
    def __init__(self, dt):
        self.N = 0
        self.vehicles = []
        self.initialized = False
        self.positions = []
        self.velocities = []
        self.dt = dt

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        self.N = self.N + 1

    def calculate_speed_difference(self, y, i):
        return y[i+self.N] - y[(i+1) % self.N+self.N]

    def calculate_distance(self, y, i):
        if i == self.N-1:
            return y[0] - y[self.N-1] + 1.
        return y[i+1] - y[i]

    def create_right_hand_side(self, t, y):
        acceleration = np.zeros(self.N)
        for i in range(self.N):
            vehicle = self.vehicles[i]
            acceleration[i] = vehicle.a*(1. - np.power(y[self.N+i]/vehicle.v_0, vehicle.delta)
                                      - np.power(vehicle.get_desired_distance(y[self.N+i], self.calculate_speed_difference(y, i))/self.calculate_distance(y, i), 2))
        return np.concatenate((y[self.N:], acceleration))

    def initialize(self, positions, velocities):
        self.positions = positions
        self.velocities = velocities
        self.initialized = True

    def initialize_uniformly(self):
        self.positions = [i/self.N for i in range(self.N)]
        self.velocities = np.zeros(self.N)
        self.initialized = True

    def simulate(self, time_discretization_scheme, final_time):
        if not self.initialized:
            self.initialize_uniformly()

        times = np.linspace(0, final_time, final_time / self.dt)

        y = np.concatenate((self.positions, self.velocities))

        for t in times:
            y = time_discretization_scheme.apply(t, self.dt, y)
            tmp = np.floor(y[0:self.N])
            y = np.concatenate((y[0:self.N]-tmp, y[self.N:]))
        return y

    def simulate_one_step(self, time_discretization_scheme, t, y):
        y = time_discretization_scheme.apply(t, self.dt, y)
        tmp = np.floor(y[0:self.N])
        y = np.concatenate((y[0:self.N]-tmp, y[self.N:]))
        return y
