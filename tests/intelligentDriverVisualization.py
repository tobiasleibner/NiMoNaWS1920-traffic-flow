import sys
sys.path.append('../')
import trafficFlow.carFollowingModel.intelligentDriver as IntDriver
import trafficFlow.utilities.eulerSchemes as EulerSchemes
import trafficFlow.graphics.circularRoad as Graphics

import numpy as np


factor = 100.

vehicle1 = IntDriver.VehicleIntelligentDriver(7./factor, 30./factor, 4./factor, 1./factor, 1./factor, 1.5/factor)
vehicle2 = IntDriver.VehicleIntelligentDriver(7./factor, 30./factor, 4./factor, 1./factor, 1./factor, 1.5/factor)
vehicle3 = IntDriver.VehicleIntelligentDriver(7./factor, 60./factor, 4./factor, 1./factor, 1./factor, 1.5/factor)

dt = 0.001

model = IntDriver.IntelligentDriverModel(dt)
model.add_vehicle(vehicle1)
model.add_vehicle(vehicle2)
model.add_vehicle(vehicle3)

eulerScheme = EulerSchemes.ExplicitEulerScheme(model.create_right_hand_side)

model.initialize_uniformly()

simulation = Graphics.CircularRoadSimulation(model=model, time_discretization_scheme=eulerScheme, dt=dt)
simulation.master.title('Circular Road Simulation')
simulation.start()
