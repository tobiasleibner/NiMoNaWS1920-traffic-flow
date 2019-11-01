class BaseDriver:
    def __init__(self):
        self.road = None
        self.velocity = 0.
        self.position = 0.
        self.predecessor = None
        self.successor = None

    def get_desired_acceleration(self):
        raise NotImplementedError
