import traci
import random
from sumolib import checkBinary
import os
def km_per_hr_to_m_per_s(km_per_hr):
    # Conversion factor from km/hr to m/s
    conversion_factor = 0.277778
    # Convert km/hr to m/s
    m_per_s = km_per_hr * conversion_factor
    return m_per_s

def run():
    step = 1
    while step<=10000:
        traci.simulationStep()
        if (step%200==0):
            # change the speed of random vehicle
            vehicle_ids = traci.vehicle.getIDList()
            random_vehicle = random.choice(vehicle_ids)
            curr_speed = traci.vehicle.getSpeed(random_vehicle)
            print(step)
            print(f"changing the speed of vehicle {random_vehicle} from {curr_speed}m/s to {curr_speed+2}m/s")
            traci.vehicle.setSpeed(random_vehicle,str(curr_speed+2))
        step+=1
if __name__=="__main__":
    
    sumo_binary = checkBinary('sumo-gui')

    # Start SUMO as a subprocess and connect with TraCI
    traci.start([sumo_binary, "-c", "./assets/maps/New/octagon.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])
    run()