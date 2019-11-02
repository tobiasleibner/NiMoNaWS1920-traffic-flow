class BaseTimeDiscretizationScheme:
    """
    Base class for time discretization schemes

    Methods
    -------
    apply(t, dt, y_old)
        performs a single time step and returns the new iterate
    """

    def apply(self, t, dt, y_old):
        raise NotImplementedError
