try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

from .baseRoadSimulation import BaseRoadSimulation


class CircularRoadSimulation(BaseRoadSimulation):
    """
    Class to model a circular road and perform the simulation on the circle

    Inherits from the BaseRoadSimulation class.

    Attributes
    ----------
    tx : double
        x coordinate of the center of the circle
    ty : double
        y coordinate of the center of the circle
    full_extent : double
        full extent of the circle
    oval_id1 : Oval
        outer oval modeling the road
    oval_id2 : Oval
        inner oval modeling the road
    running : bool
        determine whether the simulation is actually running or not
    steps : int
        number of steps performed until now
    time : double
        time expired until now
    timesteps_per_simulationstep : int
        time steps to perform before updating the visualization (depends on the time step size dt)

    Methods
    -------
    start(interval)
        override method in class BaseRoadSimulation and setup the vehicles and the time banner
    step(delta)
        override method in class BaseRoadSimulation and perform a single step of the simulation,
        update the positions of the cars according to the changes made when simulating a single
        step in the model
    toggle_pause()
        stop simulation and continue it
    """

    def __init__(self, canvas, x0, y0, x1, y1, model, time_discretization_scheme, lane_width=20, dt=1e-1):
        super().__init__(canvas, x0, y0, x1, y1, model, time_discretization_scheme, lane_width, dt)

        self.x0, self.y0, self.x1, self.y1 = x0+lane_width, y0+lane_width, x1-lane_width, y1-lane_width
        self.tx, self.ty = (x1+x0) / 2, (y1+y0) / 2
        self.full_extent = 360
        lane_width2 = lane_width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-lane_width2, self.y0-lane_width2,
                                                self.x1+lane_width2, self.y1+lane_width2)
        self.oval_id2 = self.canvas.create_oval(self.x0+lane_width2, self.y0+lane_width2,
                                                self.x1-lane_width2, self.y1-lane_width2)
        self.running = False
        self.steps = 0
        self.time = 0.0
        self.timesteps_per_simulationstep = int(0.25/dt)

    def start(self, interval=50):
        self.interval = interval
        self.increment = self.full_extent / interval
        self.extent = 0

        for vehicle in self.model.road.vehicles:
            vehicle.object_in_visualization = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                                                     start=vehicle.position * self.full_extent / self.model.road.full_length,
                                                                     extent=vehicle.length,
                                                                     width=self.lane_width,
                                                                     style='arc')

        t = 't = ' + str(int(self.time))
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=t, font=self.custom_font)
        self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        if self.running:
            for i in range(self.timesteps_per_simulationstep):
                self.steps = self.steps + 1
                self.time = self.time + self.dt
                self.model.simulate_one_step(self.time_discretization_scheme, self.time, self.dt)

            for vehicle in self.model.road.vehicles:
                self.canvas.itemconfigure(vehicle.object_in_visualization,
                                          start=vehicle.position * self.full_extent / self.model.road.full_length)

            t = 't = ' + str(int(self.time))
            self.canvas.itemconfigure(self.label_id, text=t)

        self.after_id = self.canvas.after(self.interval, self.step, delta)

    def toggle_pause(self):
        self.running = not self.running
