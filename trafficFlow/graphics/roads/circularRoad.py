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
    running : bool
        determine whether the simulation is actually running or not
    time : double
        time expired until now

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

        self.canvas.create_oval(self.x0-lane_width2, self.y0-lane_width2,
                                self.x1+lane_width2, self.y1+lane_width2)
        for i in range(self.model.road.get_number_of_lanes()):
            self.canvas.create_oval(self.x0+lane_width2+lane_width*i, self.y0+lane_width2+lane_width*i,
                                    self.x1-lane_width2-lane_width*i, self.y1-lane_width2-lane_width*i)

        self.interval = int(self.dt * 1000)
        self.label = None

        self.running = False
        self.time = 0.0

    def start(self):
        for i, lane in enumerate(self.model.road.lanes):
            for vehicle in lane.vehicles:
                shift = self.lane_width * (self.model.road.get_number_of_lanes() - 1 - i)
                vehicle.object_in_visualization = self.canvas.create_arc(
                    self.x0 + shift,
                    self.y0 + shift,
                    self.x1 - shift,
                    self.y1 - shift,
                    start=vehicle.position * self.full_extent / lane.full_length,
                    extent=vehicle.length * self.full_extent / lane.full_length,
                    width=self.lane_width,
                    style='arc')

        t = 't = ' + str(int(self.time))
        self.label = self.canvas.create_text(self.tx, self.ty, text=t, font=self.custom_font)

        self.canvas.after(self.interval, self.step)

    def step(self):
        if self.running:
            self.time = self.time + self.dt
            self.model.simulate_one_step(self.time_discretization_scheme, self.time, self.dt)

            for i, lane in enumerate(self.model.road.lanes):
                for vehicle in lane.vehicles:
                    self.canvas.delete(vehicle.object_in_visualization)
                    shift = self.lane_width * (self.model.road.get_number_of_lanes() - 1 - i)
                    vehicle.object_in_visualization = self.canvas.create_arc(
                        self.x0 + shift,
                        self.y0 + shift,
                        self.x1 - shift,
                        self.y1 - shift,
                        start=vehicle.position * self.full_extent / lane.full_length,
                        extent=vehicle.length * self.full_extent / lane.full_length,
                        width=self.lane_width,
                        style='arc')

            t = 't = ' + str(int(self.time))
            self.canvas.itemconfigure(self.label, text=t)

        self.canvas.after(self.interval, self.step)

    def toggle_pause(self):
        self.running = not self.running
