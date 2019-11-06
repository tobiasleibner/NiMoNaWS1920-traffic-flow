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

    def __init__(self):
        self.number_of_vehicles = 0
        self.road = None
        self.vehicles = []
        self.initialized = False

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.lane = self
        self.number_of_vehicles = self.number_of_vehicles + 1

    def initialize_default(self):
        raise NotImplementedError
