from trafficFlow.utilities.timeDiscretizationSchemes.baseTimeDiscretizationScheme import BaseTimeDiscretizationScheme


class ExplicitEulerScheme(BaseTimeDiscretizationScheme):
    """
    Class that implements the explicit Euler scheme to solve ordinary differential equations

    Inherits from the BaseTimeDiscretizationScheme class.

    Attributes
    ----------
    function : Function
        function to use as right hand side of the ordinary differential equation

    Methods
    -------
    apply(t, dt, y_old)
        override method in class BaseTimeDiscretizationScheme and perform a single step of the explicit Euler scheme
    """
    def __init__(self, function):
        self.function = function

    def apply(self, t, dt, y_old):
        return y_old + dt * self.function(t, y_old)
