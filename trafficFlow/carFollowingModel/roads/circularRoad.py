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

    def get_distance(self, position1, position2, lane1, lane2):
        if lane1 == lane2:
            if position1 < position2:
                return position1 - position2 + lane1.full_length
            return position1 - position2
        else:
            ###########################################################
            raise NotImplementedError

    def get_position(self, position, lane):
        if position < lane.full_length:
            return position
        return position - lane.full_length
