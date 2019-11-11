class BaseLane:
    """
    Base class for lanes used in the car following model

    Attributes
    ----------
    number_of_vehicles : int
        number of vehicles on the lane
    road : Road
        road on which the lane is located
    vehicles : list(Vehicles)
        vehicles on the lane
    initialized : bool
        true if the vehicles are already placed, false if not

    Methods
    -------
    add_vehicle(vehicle)
        add the vehicle to the lane
    initialize_default()
        place the vehicles in a default manner on the lane
    """

    def __init__(self, full_length=1000.):
        self.full_length = full_length
        self.number_of_vehicles = 0
        self.road = None
        self.vehicles = []
        self.lane_right = None
        self.lane_left = None
        self.initialized = False

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.lane = self
        self.number_of_vehicles = self.number_of_vehicles + 1

    def lane_changes(self):
        for vehicle in self.vehicles:
            vehicle.lane_change()

    def initialize_default(self):
        raise NotImplementedError
