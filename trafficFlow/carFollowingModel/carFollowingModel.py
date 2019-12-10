import numpy as np


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

    def create_right_hand_side(self, t, y):
        acceleration = []
        for lane in self.road.lanes:
            for vehicle in lane.vehicles:
                acceleration.append(vehicle.get_desired_acceleration())
        return np.concatenate((y[self.road.get_number_of_vehicles():], acceleration))

    def simulate_one_step(self, time_discretization_scheme, t, dt):
        # get total number of vehicles
        num_vehicles = self.road.get_number_of_vehicles()
        # fill current state for time discretization scheme
        y = []
        for vehicle in self.road.get_vehicles():
            y = np.append(y, vehicle.position)
        for vehicle in self.road.get_vehicles():
            y = np.append(y, vehicle.velocity)
        # perform a single time step
        y = time_discretization_scheme.apply(t, dt, y)
        # extract positions and velocities
        positions = y[:num_vehicles]
        velocities = y[num_vehicles:]
        # set negative velocities to zero
        velocities[velocities < 0.] = 0.
        # update vehicles
        for i, vehicle in enumerate(self.road.get_vehicles()):
            if self.road.get_position(positions[i], vehicle.lane) is not None:
                vehicle.position, vehicle.velocity = self.road.get_position(positions[i], vehicle.lane), velocities[i]
            else:
                vehicle.lane.remove_vehicle_by_index(i)
        # lane changes
        self.road.lane_changes()
