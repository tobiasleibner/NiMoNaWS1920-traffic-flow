import sys
sys.path.append('../')
import trafficFlow.carFollowingModel.carFollowingModel as CarFollowingModel
import trafficFlow.carFollowingModel.drivers.intelligentDriver as IntelligentDriver
import trafficFlow.carFollowingModel.roads.roads as Roads
import trafficFlow.utilities.eulerSchemes as EulerSchemes
import trafficFlow.graphics.circularRoad as CircularRoad
import trafficFlow.graphics.roadSimulation as RoadSimulation


circularRoad = Roads.CircularRoad()

vehicle1 = IntelligentDriver.IntelligentDriver(s_0=70., v_0=30., delta=4., T=1., a=1., b=1.5)
vehicle2 = IntelligentDriver.IntelligentDriver(s_0=70., v_0=30., delta=4., T=1., a=1., b=1.5)
vehicle3 = IntelligentDriver.IntelligentDriver(s_0=70., v_0=40., delta=4., T=1., a=1., b=1.5)

circularRoad.add_vehicle(vehicle1)
circularRoad.add_vehicle(vehicle2)
circularRoad.add_vehicle(vehicle3)

circularRoad.initialize_uniformly()


dt = 1e-1

model = CarFollowingModel.CarFollowingModel(circularRoad, dt)

eulerScheme = EulerSchemes.ExplicitEulerScheme(model.create_right_hand_side)

simulation = RoadSimulation.RoadSimulation(RoadType=CircularRoad.CircularRoadSimulation, model=model, time_discretization_scheme=eulerScheme, dt=dt)
simulation.master.title('Circular Road Simulation')
simulation.start()
