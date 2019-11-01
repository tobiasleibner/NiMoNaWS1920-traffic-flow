# Notwendige Imports
from trafficFlow.utilities.timeDiscretizationSchemes.baseTimeDiscretizationScheme import BaseTimeDiscretizationScheme

from scipy.optimize import root
import numpy as np


# Klasse für das explizite Euler-Verfahren
class ExplicitEulerScheme(BaseTimeDiscretizationScheme):
    # Konstruktor, der die rechte Seite der ODE als Parameter function übergeben bekommt
    def __init__(self, function):
        self.function = function

    # Funktion, die einen Schritt des expliziten Euler-Verfahrens ausführt
    def apply(self, t, dt, y_old):
        return y_old + dt * self.function(t, y_old)


# Klasse für das implizite Euler-Verfahren
class ImplicitEulerScheme(BaseTimeDiscretizationScheme):
    # Konstruktor, der die rechte Seite (function) sowie deren Ableitung (jacobian) übergeben bekommt
    def __init__(self, function, jacobian):
        self.function = function
        self.jacobian = jacobian

    # Funktion, deren Nullstelle mittels scipy.optimize.root bestimmt werden soll (Umformulierung der Iterationsvorschrift des 
    # impliziten Euler-Verfahrens in ein Nullstellenproblem)
    def root_function(self, x, t, dt, y_old):
        return x - dt * self.function(t+dt, x) - y_old

    # Ableitung der Funktion rootFunction (wird bei scipy.optimize.root benötigt)
    def root_jacobian(self, x, t, dt, y_old):
        return np.eye(len(x)) - dt * self.jacobian(t+dt, x)

    # Funktion, die einen Schritt des impliziten Euler-Verfahrens ausführt
    def apply(self, t, dt, y_old):
        return root(self.root_function, y_old, (t, dt, y_old), jac=self.root_jacobian).x
