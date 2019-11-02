class BaseRoad:
    """
    Base class for roads used in the car following model

    Attributes
    ----------
    number_of_vehicles : int
        total number of vehicles on the road (on all lanes together)
    vehicles : list(Driver)
        drivers/vehicles on the road
    initialized : bool
        true if the vehicles are already placed, false if not

    Methods
    -------
    add_vehicle(vehicle)
        add a vehicle to the road
    initialize(positions, velocities)
        initialize the vehicles using the given positions and velocities
    initialize_default()
        initialize the vehicles with default values for position and velocity
    get_distance(position1, position2)
        get the distance between position1 and position2 on the road (e.g. in the circular case the distance
        has to be calculated more carefully)
    get_position(position)
        transforms a given position to the position on the road (e.g. in the circular case the position
        has to be calculated more carefully)
    """

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
