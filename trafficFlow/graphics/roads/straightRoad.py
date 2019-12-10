try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

from PIL import ImageTk, Image
import numpy as np

from .baseRoadSimulation import BaseRoadSimulation


class StraightRoadSimulation(BaseRoadSimulation):
    """
    Class to model a circular road and perform the simulation on the circle

    Inherits from the BaseRoadSimulation class.

    Attributes
    ----------
    tx : double
        x coordinate of the center of the circle
    ty : double
        y coordinate of the center of the circle
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

    def __init__(self, canvas, x0, y0, x1, y1, model, time_discretization_scheme, lane_width=30, dt=1e-1):
        super().__init__(canvas, x0, y0, x1, y1, model, time_discretization_scheme, lane_width, dt)

        self.x0, self.y0, self.x1, self.y1 = x0+lane_width, y0+lane_width, x1-lane_width, y1-lane_width
        self.tx, self.ty = (x1+x0) / 2, (y1+y0) / 2
        self.lane_width = lane_width

        self.canvas.create_line(self.x0, self.y0, self.x1, self.x0)
        for i in range(self.model.road.get_number_of_lanes()):
            self.canvas.create_line(self.x0, self.y0 + lane_width * (i + 1), self.x1, self.y0 + lane_width * (i + 1))

        self.interval = int(self.dt * 1000)
        self.label = None

        self.running = False
        self.time = 0.0

    def start(self):
        for i, lane in enumerate(self.model.road.lanes):
            for vehicle in lane.vehicles:
                vehicle.image_temp = Image.open('../trafficFlow/graphics/images/vehicles/' + vehicle.filename)\
                    .convert("RGBA")
                new_height = self.lane_width * 5
                new_width = int(new_height / vehicle.image_temp.size[0] * vehicle.image_temp.size[1])
                vehicle.image = ImageTk.PhotoImage(vehicle.image_temp.resize((new_width, new_height)))
                vehicle.object_in_visualization = self.canvas.create_image(
                    self.x0 + vehicle.position * (self.x1 - self.x0) / lane.full_length,
                    self.y0 + self.lane_width * (i + .5),
                    image=vehicle.image)

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
                    vehicle.object_in_visualization = self.canvas.create_image(
                        self.x0 + vehicle.position * (self.x1 - self.x0) / lane.full_length,
                        self.y0 + self.lane_width * (i + .5),
                        image=vehicle.image)

            t = 't = ' + str(int(self.time))
            self.canvas.itemconfigure(self.label, text=t)

        self.canvas.after(self.interval, self.step)

    def toggle_pause(self):
        self.running = not self.running
