try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk


import numpy as np


class CircularRoad(object):
    def __init__(self, canvas, x0, y0, x1, y1, width=20, start_ang=0, full_extent=360, car_length=5, model=None, time_discretization_scheme=None, dt=1e-3):
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
        self.width = width
        self.start_ang = start_ang
        self.full_extent = full_extent
        # draw static bar outline
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2)
        self.running = False
        self.car_length = car_length
        self.steps = 0
        self.model = model
        self.time_discretization_scheme = time_discretization_scheme
        self.y = np.concatenate((self.model.positions, self.model.velocities))
        self.time = 0.
        self.timesteps_per_simulationstep = 500
        self.dt = dt

    def start(self, interval=100):
        self.interval = interval
        self.increment = self.full_extent / interval
        self.extent = 0
        self.vehicles = []

        for i, vehicle in enumerate(self.model.vehicles):
            self.vehicles.append(self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                                        start=self.model.positions[i]*self.full_extent, extent=self.car_length,
                                                        width=self.width, style='arc'))

        t = 't='+str(self.time)
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=t,
                                                font=self.custom_font)
        self.running = True
        self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        """Increment extent and update arc and label displaying how much completed."""
        if self.running:
            for i in range(self.timesteps_per_simulationstep):
                self.steps = self.steps + 1
                self.time = self.time + self.dt
                self.y = self.model.simulate_one_step(self.time_discretization_scheme, self.time, self.y)
            for i, vehicle in enumerate(self.model.vehicles):
                self.canvas.itemconfigure(self.vehicles[i], start=self.y[i]*self.full_extent)
            t = 't=' + str(self.time)
            self.canvas.itemconfigure(self.label_id, text=t)

        self.after_id = self.canvas.after(self.interval, self.step, delta)

    def toggle_pause(self):
        self.running = not self.running

class CircularRoadSimulation(tk.Frame):
    def __init__(self, model=None, time_discretization_scheme=None, dt=1e-3, master=None):
        tk.Frame.__init__(self, master)
        self.model = model
        self.time_discretization_scheme = time_discretization_scheme
        self.dt = dt
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self, width=500, height=500, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.road_simulation = CircularRoad(self.canvas, 0, 0, 500, 500, 20, model=self.model, time_discretization_scheme=self.time_discretization_scheme, dt=self.dt)

        self.pause_button = tk.Button(self, text='Pause', command=self.pause)
        self.pause_button.grid(row=1, column=0)
        self.quit_button = tk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=1, column=1)

    def start(self):
        self.road_simulation.start()
        self.mainloop()

    def pause(self):
        self.road_simulation.toggle_pause()
