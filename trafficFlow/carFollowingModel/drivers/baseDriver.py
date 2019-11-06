class BaseDriver:
    """
    Base class for drivers/vehicles used in the car following model

    Attributes
    ----------
    lane : Lane
        the lane this vehicle is added to (to get information on how to measure distances correctly,
        e.g. in the case of a circular road)
    length : double
        length of the vehicle (cars, trucks,...)
    velocity : double
        current velocity of the vehicle
    position : double
        current position of the vehicle
    predecessor : Driver
        predecessor on the same lane
    successor : Driver
        successor on the same lane
    predecessor_right : Driver
        predecessor on the lane to the right
    successor_right : Driver
        successor on the lane to the right
    predecessor_left : Driver
        predecessor on the lane to the left
    successor_left : Driver
        successor on the lane to the left
    object_in_visualization : Vehicle
        object used by the visualization to manage the vehicle (e.g. arc in the circular road case)

    Methods
    -------
    get_desired_acceleration()
        compute the current acceleration of the vehicle
    """

    def __init__(self):
        self.lane = None

        self.length = 4.
        self.velocity = 0.
        self.position = 0.

        self.predecessor = None
        self.successor = None

        self.predecessor_right = None
        self.successor_right = None
        self.predecessor_left = None
        self.successor_left = None

        self.object_in_visualization = None

    def get_desired_acceleration(self):
        raise NotImplementedError
