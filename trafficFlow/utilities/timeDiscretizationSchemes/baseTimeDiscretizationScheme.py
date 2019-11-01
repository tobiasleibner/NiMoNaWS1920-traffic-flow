class BaseTimeDiscretizationScheme:
    def apply(self, t, dt, y_old):
        raise NotImplementedError
