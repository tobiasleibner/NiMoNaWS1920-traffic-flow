import math


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

    def __init__(self, length=4., lane_change_safety_distance=50., label=""):
        self.lane = None

        self.label = label
        self.length = length
        self.lane_change_safety_distance = lane_change_safety_distance
        self.max_speed = 200.
        self.velocity = 0.
        self.position = 0.

        self.predecessor = None
        self.successor = None

        self.predecessor_right = None
        self.predecessor_left = None
        self.successor_right = None
        self.successor_left = None

        self.object_in_visualization = None

    def __str__(self):
        return self.label

    def get_distance_to_predecessor(self):
        if self.predecessor and not self.predecessor == self:
            return self.lane.road.get_distance(self.predecessor, self) - self.length
        else:
            return self.lane.full_length

    def get_distance_to_successor(self):
        if self.successor and not self.successor == self:
            return self.lane.road.get_distance(self, self.successor) - self.successor.length
        else:
            return self.lane.full_length

    def get_distance_to_predecessor_right(self):
        if self.predecessor_right:
            return self.lane.road.get_distance(self.predecessor_right, self) - self.length
        else:
            return self.lane.full_length

    def get_distance_to_successor_right(self):
        if self.successor_right:
            return self.lane.road.get_distance(self, self.successor_right) - self.successor_right.length
        else:
            return self.lane.full_length

    def get_distance_to_predecessor_left(self):
        if self.predecessor_left:
            return self.lane.road.get_distance(self.predecessor_left, self) - self.length
        else:
            return self.lane.full_length

    def get_distance_to_successor_left(self):
        if self.successor_left:
            return self.lane.road.get_distance(self, self.successor_left) - self.successor_left.length
        else:
            return self.lane.full_length

    def get_speed_difference_to_predecessor(self):
        if self.predecessor and not self.predecessor == self:
            return self.velocity - self.predecessor.velocity
        else:
            return -self.max_speed

    def get_speed_difference_to_successor(self):
        if self.successor and not self.successor == self:
            return self.successor.velocity - self.velocity
        else:
            return math.inf

    def get_speed_difference_to_predecessor_right(self):
        if self.predecessor_right:
            return self.velocity - self.predecessor_right.velocity
        else:
            return -math.inf

    def get_speed_difference_to_successor_right(self):
        if self.successor_right:
            return self.successor_right.velocity - self.velocity
        else:
            return math.inf

    def get_speed_difference_to_predecessor_left(self):
        if self.predecessor_left:
            return self.velocity - self.predecessor_left.velocity
        else:
            return -math.inf

    def get_speed_difference_to_successor_left(self):
        if self.successor_left:
            return self.successor_left.velocity - self.velocity
        else:
            return math.inf

    def get_desired_acceleration(self):
        raise NotImplementedError

    def lane_change(self):
        changed = False
        if self.lane.lane_right:
            if not self.predecessor_right:
                if not self.successor_right:
                    self.change_to_right_lane()
                    changed = True
                elif self.lane.road.get_distance(self, self.successor_right) >= self.lane_change_safety_distance:
                    self.change_to_right_lane()
                    changed = True
            else:
                if not self.successor_right:
                    if self.lane.road.get_distance(self.predecessor_right, self) >= self.lane_change_safety_distance:
                        self.change_to_right_lane()
                        changed = True
                elif self.lane.road.get_distance(self.predecessor_right, self) >= self.lane_change_safety_distance and self.lane.road.get_distance(self, self.successor_right) >= self.lane_change_safety_distance:
                    self.change_to_right_lane()
                    changed = True

        if not changed and self.lane.lane_left:
            if self.predecessor and self.get_distance_to_predecessor() <= self.lane_change_safety_distance and self.get_speed_difference_to_predecessor() > 0.:
                if self.predecessor_left:
                    if self.get_distance_to_predecessor_left() >= self.lane_change_safety_distance:
                        if not self.successor_left:
                            self.change_to_left_lane()
                        elif self.get_distance_to_successor_left() >= self.lane_change_safety_distance:
                            self.change_to_left_lane()
                else:
                    if not self.successor_left:
                        self.change_to_left_lane()
                    elif self.get_distance_to_successor_left() >= self.lane_change_safety_distance:
                        self.change_to_left_lane()

    def change_to_right_lane(self):
        self.lane.vehicles.remove(self)
        self.lane.lane_right.vehicles.append(self)
        self.lane = self.lane.lane_right

        if self.predecessor_left:
            self.predecessor_left.successor_right = self.successor
        if self.successor_left:
            self.successor_left.predecessor_right = self.predecessor
        if self.predecessor:
            if not self.predecessor.successor_right or (self.predecessor.successor_right and self.lane.road.between(self.predecessor, self, self.predecessor.successor_right)):
                self.predecessor.successor_right = self
            if not self.successor == self.predecessor:
                self.predecessor.successor = self.successor
            else:
                self.predecessor.successor = None
            if self.predecessor.predecessor == self:
                self.predecessor.predecessor = None
        if self.successor:
            if not self.successor.predecessor_right or (self.successor.predecessor_right and self.lane.road.between(self.successor.predecessor_right, self, self.successor)):
                self.predecessor.successor_right = self
            if not self.predecessor == self.successor:
                self.successor.predecessor = self.predecessor
            else:
                self.successor.predecessor = None
            if self.successor.successor == self:
                self.successor.successor = None
        if self.predecessor_right:
            self.predecessor_right.successor = self
            self.predecessor_right.successor_left = self.successor
            if self.predecessor_right.predecessor_left == self:
                self.predecessor_right.predecessor_left = None
        if self.successor_right:
            self.successor_right.predecessor = self
            self.successor_right.predecessor_left = self.predecessor
            if self.successor_right.successor_left == self:
                self.successor_right.successor_left = None

        self.predecessor_left = self.predecessor
        self.successor_left = self.successor
        self.predecessor = self.predecessor_right
        self.successor = self.successor_right

        if self.predecessor_right:
            self.predecessor_right = self.predecessor_right.predecessor_right
        if self.predecessor_right and self.predecessor_right.successor:
            while self.lane.road.between(self.predecessor_right, self.predecessor_right.successor, self):
                self.predecessor_right = self.predecessor_right.successor

        if self.successor_right:
            self.successor_right = self.successor_right.successor_right
        if self.successor_right and self.successor_right.predecessor:
            while self.lane.road.between(self, self.successor_right.predecessor, self.successor_right):
                self.successor_right = self.successor_right.predecessor

    def change_to_left_lane(self):
        self.lane.vehicles.remove(self)
        self.lane.lane_left.vehicles.append(self)
        self.lane = self.lane.lane_left

        if self.predecessor_right:
            self.predecessor_right.successor_left = self.successor
        if self.successor_right:
            self.successor_right.predecessor_left = self.predecessor
        if self.predecessor:
            if not self.predecessor.successor_left or (self.predecessor.successor_left and self.lane.road.between(self.predecessor, self, self.predecessor.successor_left)):
                self.predecessor.successor_left = self
            if not self.successor == self.predecessor:
                self.predecessor.successor = self.successor
            else:
                self.predecessor.successor = None
            if self.predecessor.predecessor == self:
                self.predecessor.predecessor = None
        if self.successor:
            if not self.successor.predecessor_left or (self.successor.predecessor_left and self.lane.road.between(self.successor.predecessor_left, self, self.successor)):
                self.predecessor.successor_left = self
            if not self.predecessor == self.successor:
                self.successor.predecessor = self.predecessor
            else:
                self.successor.predecessor = None
            if self.successor.successor == self:
                self.successor.successor = None
        if self.predecessor_left:
            self.predecessor_left.successor = self
            self.predecessor_left.successor_right = self.successor
            if self.predecessor_left.predecessor_right == self:
                self.predecessor_left.predecessor_right = None
        if self.successor_left:
            self.successor_left.predecessor = self
            self.successor_left.predecessor_right = self.predecessor
            if self.successor_left.successor_right == self:
                self.successor_left.successor_right = None

        self.predecessor_right = self.predecessor
        self.successor_right = self.successor
        self.predecessor = self.predecessor_left
        self.successor = self.successor_left

        if self.predecessor_left:
            self.predecessor_left = self.predecessor_left.predecessor_left
        if self.predecessor_left and self.predecessor_left.successor:
            while self.lane.road.between(self.predecessor_left, self.predecessor_left.successor, self):
                self.predecessor_left = self.predecessor_left.successor

        if self.successor_left:
            self.successor_left = self.successor_left.successor
        if self.successor_left and self.successor_left.predecessor:
            while self.lane.road.between(self, self.successor_left.predecessor, self.successor_left):
                self.successor_left = self.successor_left.predecessor
