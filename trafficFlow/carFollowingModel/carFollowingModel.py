import numpy as np


class CarFollowingModel:
    def __init__(self, road):
        self.road = road

    def create_right_hand_side(self, t, y):
        acceleration = []
        for vehicle in self.road.vehicles:
            acceleration.append(vehicle.get_desired_acceleration())
        return np.concatenate((y[self.road.number_of_vehicles:], acceleration))

    def simulate_one_step(self, time_discretization_scheme, t, dt):
        y = []
        for vehicle in self.road.vehicles:
            y.append(vehicle.position)
        for vehicle in self.road.vehicles:
            y.append(vehicle.velocity)
        y = time_discretization_scheme.apply(t, dt, y)
        for i, vehicle in enumerate(self.road.vehicles):
            vehicle.position = self.road.get_position(y[i])
            vehicle.velocity = y[self.road.number_of_vehicles + i]
