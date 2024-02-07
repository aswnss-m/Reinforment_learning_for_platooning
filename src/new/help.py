import os
import sys
import traci
import random
from sumolib import checkBinary
from time import sleep
def run():
    traci.start(sumoCmd)
    traci.simulationStep()
    # Change lane of all vehicles
    sleep(10)
    for veh_id in traci.vehicle.getIDList():
        new_lane = random.choice(traci.vehicle.getLaneID(veh_id))
        traci.vehicle.changeLane(veh_id, new_lane, 1000)

    # Change speed of all vehicles
    for veh_id in traci.vehicle.getIDList():
        new_speed = random.uniform(0, 30)  # Assuming speed limit is 30 m/s
        traci.vehicle.setSpeed(veh_id, new_speed)

    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    sumoBinary = checkBinary('sumo-gui')
    sumoCmd = [sumoBinary, "-c", "./assets/maps/New/octagon.sumocfg", "--random", "true", "--output-prefix", " TIME"]

    run()