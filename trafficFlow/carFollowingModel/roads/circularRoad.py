from .baseRoad import BaseRoad


class CircularRoad(BaseRoad):
    def __init__(self, full_length=1000.):
        super().__init__()
        self.full_length = full_length

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.road = self
        self.number_of_vehicles = self.number_of_vehicles + 1

    def initialize(self, positions, velocities):
        for i, vehicle in enumerate(self.vehicles):
            vehicle.position = positions[i]
            vehicle.velocity = velocities[i]
        self.initialized = True

    def initialize_default(self):
        for i, vehicle in enumerate(self.vehicles):
            vehicle.predecessor = self.vehicles[(i+1) % self.number_of_vehicles]
            if i == 0:
                vehicle.successor = self.vehicles[self.number_of_vehicles-1]
            else:
                vehicle.successor = self.vehicles[i-1]
            vehicle.position = i*self.full_length/self.number_of_vehicles
            vehicle.velocity = 0.
        self.initialized = True

    def get_distance(self, position1, position2):
        if position1 < position2:
            return position1 - position2 + self.full_length
        return position1 - position2

    def get_position(self, position):
        if position < self.full_length:
            return position
        return position - self.full_length
