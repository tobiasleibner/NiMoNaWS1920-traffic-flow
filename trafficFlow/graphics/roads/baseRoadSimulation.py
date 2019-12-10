try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk


class BaseRoadSimulation:
    """
    Base class for the road simulation

    Attributes
    ----------
    custom_font : tkFont.Font
        font to use in the visualization
    canvas : tk.Canvas
        canvas to draw on
    x0 : int
        x coordinate of the upper left corner of the canvas in the frame
    y0 : int
        y coordinate of the upper left corner of the canvas in the frame
    x1 : int
        x coordinate of the lower right corner of the canvas in the frame
    y1 : int
        y coordinate of the lower right corner of the canvas in the frame
    model : Model
        model to use for the simulation (e.g. the car following model)
    time_discretization_scheme : TimeDiscretizationScheme
        time discretization scheme to use for the single time steps (e.g. the explicit Euler scheme)
    lane_width : double
        width of a single lane
    dt : double
        time step size

    Methods
    -------
    start(interval)
        function that is executed when starting/initializing the simulation
    step(delta)
        function that performs the update of the scenery depending on the simulation using model
    toggle_pause()
        stop simulation and continue it
    """

    def __init__(self, canvas, x0, y0, x1, y1, model, time_discretization_scheme, lane_width=30, dt=1e-1):
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0 , self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.lane_width = lane_width

        self.model = model
        self.time_discretization_scheme = time_discretization_scheme
        self.dt = dt

    def start(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def toggle_pause(self):
        raise NotImplementedError
