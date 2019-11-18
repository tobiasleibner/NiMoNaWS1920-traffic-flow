"""
Example of intelligent drivers on a circular road

First, the road and seven drivers are created. The vehicles are added to two different lanes and
are initialized in a default manner. Then, the car following model on the circular road and the
explicit Euler scheme to solve the arising ordinary differential equation are initialized.
As the last step, the simulation is created, a title for the window is added and the simulation is started.
"""

import sys
sys.path.append('../')
import trafficFlow.carFollowingModel.carFollowingModel as CarFollowingModel
import trafficFlow.carFollowingModel.drivers.intelligentDriver as IntelligentDriver
import trafficFlow.carFollowingModel.roads.circularRoad as Road
import trafficFlow.carFollowingModel.lanes.simpleLane as Lane
import trafficFlow.utilities.timeDiscretizationSchemes.eulerSchemes as EulerSchemes
import trafficFlow.graphics.roads.circularRoad as CircularRoad
import trafficFlow.graphics.roadSimulation as RoadSimulation


circularRoad = Road.CircularRoad()

vehicle1 = IntelligentDriver.IntelligentDriver(s_0=7., v_0=26., delta=4., T=1., a=1., b=1.5, length=3., label="car")
vehicle2 = IntelligentDriver.IntelligentDriver(s_0=7., v_0=10., delta=4., T=1., a=1., b=1.5, length=8., label="truck")
vehicle3 = IntelligentDriver.IntelligentDriver(s_0=7., v_0=24., delta=4., T=1., a=1., b=1.5)

vehicle4 = IntelligentDriver.IntelligentDriver(s_0=7., v_0=20., delta=4., T=1., a=1., b=1.5, label="test")
vehicle5 = IntelligentDriver.IntelligentDriver(s_0=7., v_0=20., delta=4., T=1., a=1., b=1.5)
vehicle6 = IntelligentDriver.IntelligentDriver(s_0=7., v_0=20., delta=4., T=1., a=.9, b=1.5)
vehicle7 = IntelligentDriver.IntelligentDriver(s_0=7., v_0=26., delta=4., T=1., a=1., b=1.5)

length = 300.

lane1 = Lane.SimpleLane(full_length=length)
lane2 = Lane.SimpleLane(full_length=length)

circularRoad.add_lane(lane1)
circularRoad.add_lane(lane2)

lane1.add_vehicle(vehicle1)
lane1.add_vehicle(vehicle2)
#lane1.add_vehicle(vehicle3)

lane2.add_vehicle(vehicle4)
#lane2.add_vehicle(vehicle5)
#lane2.add_vehicle(vehicle6)
#lane2.add_vehicle(vehicle7)

circularRoad.initialize_default()

vehicle1.velocity = 20.
vehicle1.position = 20.

model = CarFollowingModel.CarFollowingModel(circularRoad)

eulerScheme = EulerSchemes.ExplicitEulerScheme(model.create_right_hand_side)

dt = 5e-2

simulation = RoadSimulation.RoadSimulation(RoadType=CircularRoad.CircularRoadSimulation,
                                           model=model,
                                           time_discretization_scheme=eulerScheme,
                                           dt=dt)
simulation.master.title("Circular Road Intelligent Driver Simulation")
simulation.start()
