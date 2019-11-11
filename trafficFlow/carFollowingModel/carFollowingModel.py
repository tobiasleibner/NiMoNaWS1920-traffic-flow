import numpy as np

import sys
sys.path.append('../')
import trafficFlow.utilities.exceptions as Exceptions


class CarFollowingModel:
    """
    Class that implements the simulation of one step of the car following model

    Attributes
    ----------
    road : Road
        the road to simulate on (needed to get the vehicles, the number of vehicles and correct positions)

    Methods
    -------
    create_right_hand_side(t, y)
        computes right hand side of the ordinary differential equation using the desired acceleration of the vehicles
        and the current value of the solution
    simulate_one_step(time_discretization_scheme, t, dt)
        simulate a single step of the car following model using a time step of length dt
        and update position and velocity of the vehicles
    """

    def __init__(self, road):
        self.road = road
        if not self.road.initialized:
            raise Exceptions.NotInitializedError('The road has not been initialized, so the vehicles are not placed...')

    def create_right_hand_side(self, t, y):
        acceleration = []
        for lane in self.road.lanes:
            for vehicle in lane.vehicles:
                acceleration.append(vehicle.get_desired_acceleration())
        return np.concatenate((y[self.road.get_number_of_vehicles():], acceleration))

    def simulate_one_step(self, time_discretization_scheme, t, dt):
        y = []
        for vehicle in self.road.get_vehicles():
            y.append(vehicle.position)
        for vehicle in self.road.get_vehicles():
            y.append(vehicle.velocity)
        y = time_discretization_scheme.apply(t, dt, y)
        for i, vehicle in enumerate(self.road.get_vehicles()):
            vehicle.position = self.road.get_position(y[i], vehicle.lane)
            if y[self.road.get_number_of_vehicles() + i] < 0.:
                vehicle.velocity = 0.
            else:
                vehicle.velocity = y[self.road.get_number_of_vehicles() + i]
        self.road.update_data()
