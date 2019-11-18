from .baseRoad import BaseRoad


class CircularRoad(BaseRoad):
    """
    Class implementing the circular road (handling of vehicles etc., not the visualization)

    Inherits from the BaseRoad class.

    Methods
    -------
    get_distance(position1, position2)
        override method in class BaseRoad and compute distance with special treatment of circular geometry
    get_position(position)
        override method in class BaseRoad and return the correct position on the circle
    """

    def __init__(self):
        super().__init__()

    def get_position(self, position, lane):
        if position < lane.full_length:
            return position
        return position - lane.full_length

    def get_distance(self, vehicle1, vehicle2):
        if not vehicle1:
            return vehicle2.lane.full_length  # math.inf
        if not vehicle2:
            return vehicle1.lane.full_length  # math.inf
        if vehicle1.position >= vehicle2.position:
            return vehicle1.position - vehicle2.position
        else:
            return vehicle1.position - vehicle2.position + vehicle1.lane.full_length

    def between(self, first, second, third):
        if first >= second and (second >= third or third >= first):
            return True
        if first < second and first <= third <= second:
            return True
        return False
