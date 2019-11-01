try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

import numpy as np


class CircularRoadSimulation(object):
    def __init__(self, canvas, x0, y0, x1, y1, lane_width=20, car_length=5, model=None, time_discretization_scheme=None, dt=1e-1):
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+lane_width, y0+lane_width, x1-lane_width, y1-lane_width
        self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
        self.lane_width = lane_width
        self.start_ang = 0
        self.full_extent = 360
        # draw static bar outline
        w2 = lane_width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2)
        self.running = False
        self.car_length = car_length
        self.steps = 0
        self.model = model
        self.time_discretization_scheme = time_discretization_scheme
        self.time = 0.
        self.timesteps_per_simulationstep = int(0.5/dt)
        self.dt = dt

    def start(self, interval=100):
        self.interval = interval
        self.increment = self.full_extent / interval
        self.extent = 0
        self.vehicles = []

        for vehicle in self.model.road.vehicles:
            self.vehicles.append(self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                                        start=vehicle.position*self.full_extent/self.model.road.full_length, extent=self.car_length,
                                                        width=self.lane_width, style='arc'))

        t = 't = ' + str(int(self.time))
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=t, font=self.custom_font)
        self.running = True
        self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        """Increment extent and update arc and label displaying how much completed."""
        if self.running:
            for i in range(self.timesteps_per_simulationstep):
                self.steps = self.steps + 1
                self.time = self.time + self.dt
                self.model.simulate_one_step(self.time_discretization_scheme, self.time)
            for i, vehicle in enumerate(self.model.road.vehicles):
                self.canvas.itemconfigure(self.vehicles[i], start=vehicle.position*self.full_extent/self.model.road.full_length)
            t = 't = ' + str(int(self.time))
            self.canvas.itemconfigure(self.label_id, text=t)

        self.after_id = self.canvas.after(self.interval, self.step, delta)

    def toggle_pause(self):
        self.running = not self.running
