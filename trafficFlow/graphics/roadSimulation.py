try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk


class RoadSimulation(tk.Frame):
    """
    Class that creates a new tk.Frame, adds some widgets to control the simulation and runs the simulation

    Inherits from the tk.Frame class.

    Attributes
    ----------
    RoadType : RoadSimulation (class name)
        class to use as road model
    model : Model
        model to use for the simulation (e.g. the car following model)
    time_discretization_scheme : TimeDiscretizationScheme
        time discretization scheme to use for the single time steps (e.g. the explicit Euler scheme)
    dt : double
        time step size
    width : double
        width of the frame
    height : double
        height of the frame
    canvas : tk.Canvas
        canvas to add the road and the buttons to
    road_simulation : RoadSimulation (object)
        object of type RoadType to handle the simulation
    start_button : tk.Button
        button to start the simulation
    pause_button : tk.Button
        button to pause the simulation
    quit_button : tk.Button
        button to quit the simulation and close the window

    Methods
    -------
    create_widgets()
        create and add the widgets (buttons, canvas for simulation,...)
    start()
        execute when the frame is initialized (setup canvas and add vehicles etc.)
    start_simulation()
        execute on button click and start running the simulation
    pause()
        execute on button click and interrupt the simulation
    """

    def __init__(self, RoadType, model, time_discretization_scheme, dt=1e-1, master=None):
        tk.Frame.__init__(self, master)
        self.RoadType = RoadType
        self.model = model
        self.time_discretization_scheme = time_discretization_scheme
        self.dt = dt
        self.width = 500
        self.height = 500

        self.canvas = None
        self.road_simulation = None
        self.start_button = None
        self.pause_button = None
        self.quit_button = None

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.road_simulation = self.RoadType(self.canvas, 0, 0, self.width, self.height, model=self.model,
                                             time_discretization_scheme=self.time_discretization_scheme,
                                             lane_width=20, dt=self.dt)

        self.start_button = tk.Button(self, text='Start', command=self.start_simulation)
        self.start_button.grid(row=1, column=0)
        self.pause_button = tk.Button(self, text='Pause', command=self.pause)
        self.pause_button.grid(row=1, column=1)
        self.quit_button = tk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=1, column=2)

    def start(self):
        self.road_simulation.start()
        self.mainloop()

    def start_simulation(self):
        if not self.road_simulation.running:
            self.road_simulation.running = True

    def pause(self):
        self.road_simulation.toggle_pause()
