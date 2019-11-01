class BaseRoad:
    def __init__(self):
        self.number_of_vehicles = 0
        self.vehicles = []
        self.initialized = False

    def add_vehicle(self, vehicle):
        raise NotImplementedError

    def initialize(self, positions, velocities):
        raise NotImplementedError

    def initialize_default(self):
        raise NotImplementedError

    def get_distance(self, position1, position2):
        raise NotImplementedError

    def get_position(self, position):
        raise NotImplementedError
