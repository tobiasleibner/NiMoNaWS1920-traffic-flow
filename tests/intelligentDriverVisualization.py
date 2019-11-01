import sys
sys.path.append('../')
import trafficFlow.carFollowingModel.carFollowingModel as CarFollowingModel
import trafficFlow.carFollowingModel.drivers.intelligentDriver as IntelligentDriver
import trafficFlow.carFollowingModel.roads.circularRoad as Roads
import trafficFlow.utilities.timeDiscretizationSchemes.eulerSchemes as EulerSchemes
import trafficFlow.graphics.roads.circularRoad as CircularRoad
import trafficFlow.graphics.roadSimulation as RoadSimulation


circularRoad = Roads.CircularRoad()

vehicle1 = IntelligentDriver.IntelligentDriver(s_0=70., v_0=30., delta=4., T=1., a=1., b=1.5)
vehicle2 = IntelligentDriver.IntelligentDriver(s_0=70., v_0=30., delta=4., T=1., a=1., b=1.5)
vehicle3 = IntelligentDriver.IntelligentDriver(s_0=70., v_0=40., delta=4., T=1., a=1., b=1.5)

circularRoad.add_vehicle(vehicle1)
circularRoad.add_vehicle(vehicle2)
circularRoad.add_vehicle(vehicle3)

circularRoad.initialize_default()

model = CarFollowingModel.CarFollowingModel(circularRoad)

eulerScheme = EulerSchemes.ExplicitEulerScheme(model.create_right_hand_side)

dt = 1e-1

simulation = RoadSimulation.RoadSimulation(RoadType=CircularRoad.CircularRoadSimulation, model=model, time_discretization_scheme=eulerScheme, dt=dt)
simulation.master.title('Circular Road Simulation')
simulation.start()
