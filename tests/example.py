import sys
sys.path.append('../')
import trafficFlow.carFollowingModel.intelligentDriver as IntDriver
import trafficFlow.utilities.eulerSchemes as EulerSchemes

factor = 100.

vehicle1 = IntDriver.VehicleIntelligentDriver(5./factor, 50./factor, 4./factor, 1./factor, 1./factor, 1.5/factor)
vehicle2 = IntDriver.VehicleIntelligentDriver(5./factor, 50./factor, 4./factor, 1./factor, 1./factor, 1.5/factor)

final_time = 100.
dt = 0.001

model = IntDriver.IntelligentDriverModel(dt)
model.add_vehicle(vehicle1)
model.add_vehicle(vehicle2)

eulerScheme = EulerSchemes.ExplicitEulerScheme(model.create_right_hand_side)

res = model.simulate(eulerScheme, final_time)

print(res)
