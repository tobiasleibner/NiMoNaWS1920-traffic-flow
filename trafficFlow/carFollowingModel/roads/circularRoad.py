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

    def get_distance(self, vehicle1, vehicle2):
        if vehicle1.position >= vehicle2.position:
            return vehicle1.position - vehicle2.position
        else:
            return vehicle1.position - vehicle2.position + vehicle1.lane.full_length

    def get_position(self, position, lane):
        if position < lane.full_length:
            return position
        return position - lane.full_length

    def between(self, first, second, third):
        if first.position >= second.position and (second.position >= third.position or third.position >= first.position):
            return True
        if first.position < second.position and first.position <= third.position <= second.position:
            return True
        return False

    def in_front(self, predecessor, successor):
        if predecessor.position >= successor.position:
            if predecessor.position - successor.position <= predecessor.lane.full_length/2.:
                return True
        else:
            if successor.position - predecessor.position >= predecessor.lane.full_length/2.:
                return True
        return False

    def update_data(self):
        for lane in self.lanes:
            lane.lane_changes()

            for vehicle in lane.vehicles:
                changed = False
                if vehicle.predecessor_right and vehicle.successor_right and vehicle.predecessor_right == vehicle.successor_right:
                    if lane.road.in_front(vehicle, vehicle.predecessor_right):
                        if not vehicle.predecessor_right.predecessor_left == vehicle:
                            vehicle.predecessor_right.predecessor_left = vehicle
                            vehicle.predecessor_right.successor_left = vehicle.successor
                        changed = True
                    if not changed and vehicle.successor_right:
                        if lane.road.in_front(vehicle.successor_right, vehicle):
                            if not vehicle.successor_right.successor_left == vehicle:
                                vehicle.successor_right.successor_left = vehicle
                                vehicle.successor_right.predecessor_left = vehicle.predecessor
                else:
                    if vehicle.predecessor_right:
                        if lane.road.in_front(vehicle, vehicle.predecessor_right):
                            if not vehicle.predecessor_right.predecessor_left == vehicle:
                                vehicle.predecessor_right.predecessor_left = vehicle
                                vehicle.predecessor_right.successor_left = vehicle.successor
                            if not vehicle.successor_right == vehicle.predecessor_right:
                                vehicle.successor_right = vehicle.predecessor_right
                                vehicle.predecessor_right = vehicle.predecessor_right.predecessor
                            changed = True
                    if not changed and vehicle.successor_right:
                        if lane.road.in_front(vehicle.successor_right, vehicle):
                            if not vehicle.successor_right.successor_left == vehicle:
                                vehicle.successor_right.successor_left = vehicle
                                vehicle.successor_right.predecessor_left = vehicle.predecessor
                            if not vehicle.predecessor_right == vehicle.successor_right:
                                vehicle.predecessor_right = vehicle.successor_right
                                vehicle.successor_right = vehicle.successor_right.successor

    def initialize_predecessors_successors_right_left(self):
        return
        if self.number_of_lanes > 1:
            for i, lane in enumerate(self.lanes):
                if i == 0:
                    # initialize predecessor_right and successor_right
                    if lane.lane_right.number_of_vehicles > 0:
                        for vehicle in lane.vehicles:
                            vehicle.predecessor_right = lane.lane_right.vehicles[0]
                            if lane.road.in_front(vehicle.predecessor_right,
                                                  vehicle):
                                while vehicle.predecessor_right.successor and lane.road.in_front(
                                        vehicle.predecessor_right.successor,
                                        vehicle):
                                    vehicle.predecessor_right = vehicle.predecessor_right.successor
                            else:
                                while vehicle.predecessor_right.predecessor and lane.road.in_front(
                                        vehicle,
                                        vehicle.predecessor_right.predecessor):
                                    vehicle.predecessor_right = vehicle.predecessor_right.predecessor
                        for vehicle in lane.vehicles:
                            if vehicle.predecessor_right.successor:
                                vehicle.successor_right = vehicle.predecessor_right.successor
                            else:
                                vehicle.successor_right = vehicle.predecessor_right
                elif i == self.number_of_lanes - 1:
                    # initialize predecessor_left and successor_left
                    if lane.lane_left.number_of_vehicles > 0:
                        for vehicle in lane.vehicles:
                            vehicle.predecessor_left = lane.lane_left.vehicles[0]
                            if lane.road.in_front(vehicle.predecessor_left,
                                                  vehicle):
                                while vehicle.predecessor_left.successor and lane.road.in_front(
                                        vehicle.predecessor_left.successor,
                                        vehicle):
                                    vehicle.predecessor_left = vehicle.predecessor_left.successor
                            else:
                                while vehicle.predecessor_left.predecessor and lane.road.in_front(
                                        vehicle,
                                        vehicle.predecessor_left.predecessor):
                                    vehicle.predecessor_left = vehicle.predecessor_left.predecessor
                        for vehicle in lane.vehicles:
                            if vehicle.predecessor_left.successor:
                                vehicle.successor_left = vehicle.predecessor_left.successor
                            else:
                                vehicle.successor_left = vehicle.predecessor_left
                else:
                    # initialize predecessor_right, successor_right, predecessor_left and successor_left
                    if lane.lane_right.number_of_vehicles > 0:
                        for vehicle in lane.vehicles:
                            vehicle.predecessor_right = lane.lane_right.vehicles[0]
                            if lane.road.in_front(vehicle.predecessor_right,
                                                  vehicle):
                                while vehicle.predecessor_right.successor and lane.road.in_front(
                                        vehicle.predecessor_right.successor,
                                        vehicle):
                                    vehicle.predecessor_right = vehicle.predecessor_right.successor
                            else:
                                while vehicle.predecessor_right.predecessor and lane.road.in_front(
                                        vehicle,
                                        vehicle.predecessor_right.predecessor):
                                    vehicle.predecessor_right = vehicle.predecessor_right.predecessor
                        for vehicle in lane.vehicles:
                            if vehicle.predecessor_right.successor:
                                vehicle.successor_right = vehicle.predecessor_right.successor
                            else:
                                vehicle.successor_right = vehicle.predecessor_right

                    if lane.lane_left.number_of_vehicles > 0:
                        for vehicle in lane.vehicles:
                            vehicle.predecessor_left = lane.lane_left.vehicles[0]
                            if lane.road.in_front(vehicle.predecessor_left,
                                                  vehicle):
                                while vehicle.predecessor_left.successor and lane.road.in_front(
                                        vehicle.predecessor_left.successor,
                                        vehicle):
                                    vehicle.predecessor_left = vehicle.predecessor_left.successor
                            else:
                                while vehicle.predecessor_left.predecessor and lane.road.in_front(
                                        vehicle,
                                        vehicle.predecessor_left.predecessor):
                                    vehicle.predecessor_left = vehicle.predecessor_left.predecessor
                        for vehicle in lane.vehicles:
                            if vehicle.predecessor_left.successor:
                                vehicle.successor_left = vehicle.predecessor_left.successor
                            else:
                                vehicle.successor_left = vehicle.predecessor_left
