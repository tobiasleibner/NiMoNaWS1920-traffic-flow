try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk


class RoadSimulation(tk.Frame):
    def __init__(self, RoadType, model, time_discretization_scheme, dt=1e-1, master=None):
        tk.Frame.__init__(self, master)
        self.RoadType = RoadType
        self.model = model
        self.time_discretization_scheme = time_discretization_scheme
        self.dt = dt
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self, width=500, height=500, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.road_simulation = self.RoadType(self.canvas, 0, 0, 500, 500, 20, model=self.model, time_discretization_scheme=self.time_discretization_scheme, dt=self.dt)

        self.pause_button = tk.Button(self, text='Pause', command=self.pause)
        self.pause_button.grid(row=1, column=0)
        self.quit_button = tk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=1, column=1)

    def start(self):
        self.road_simulation.start()
        self.mainloop()

    def pause(self):
        self.road_simulation.toggle_pause()
