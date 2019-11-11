class BaseRoad:
    """
    Base class for roads used in the car following model

    Attributes
    ----------
    number_of_lanes : int
        total number of lanes of the road
    lanes : list(Lanes)
        lanes of the road
    initialized : bool
        true if the vehicles are already placed, false if not

    Methods
    -------
    add_lane(lane)
        add a lane to the road
    get_number_of_vehicles()
        return the overall number of vehicles on all lanes
    get_vehicles()
        return a list of all vehicles on all lanes
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
        self.number_of_lanes = 0
        self.lanes = []
        self.initialized = False

    def add_lane(self, lane):
        if self.number_of_lanes > 0:
            lane.lane_left = self.lanes[-1]
            self.lanes[-1].lane_right = lane
        self.lanes.append(lane)
        lane.road = self
        self.number_of_lanes = self.number_of_lanes + 1

    def get_number_of_vehicles(self):
        number_of_vehicles = 0
        for lane in self.lanes:
            number_of_vehicles = number_of_vehicles + lane.number_of_vehicles
        return number_of_vehicles

    def get_vehicles(self):
        vehicles = []
        for lane in self.lanes:
            vehicles.extend(lane.vehicles)
        return vehicles

    def update_data(self):
        raise NotImplementedError

    def initialize_default(self):
        for lane in self.lanes:
            lane.initialize_default()
        self.initialize_predecessors_successors_right_left()
        self.initialized = True

    def initialize_predecessors_successors_right_left(self):
        raise NotImplementedError

    def get_distance(self, vehicle1, vehicle2):
        raise NotImplementedError

    def get_position(self, position, lane):
        raise NotImplementedError

    def between(self, first, second, third):
        raise NotImplementedError

    def in_front(self, predecessor, successor):
        raise NotImplementedError
