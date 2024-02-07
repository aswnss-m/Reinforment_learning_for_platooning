
import os
import sys
import optparse
import pandas as pd

# Import necessary modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def run():
    step = 0
    data = []

    while step <= 1000:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()  # Get the list of all vehicles

        for veh_id in vehicle_ids:
            # Get vehicle information
            speed = traci.vehicle.getSpeed(veh_id)
            position = traci.vehicle.getPosition(veh_id)
            route = traci.vehicle.getRoute(veh_id)
            follower = traci.vehicle.getFollower(veh_id)
            lane = traci.vehicle.getLaneID(veh_id)
            acceleration = traci.vehicle.getAcceleration(veh_id)
            # Append the information to the data list
            data.append({
                'Step': step,
                'VehicleID': veh_id,
                'Speed': speed,
                'Position': position,
                'Route': route,
                'Follower' : follower,
                'Lane' : lane,
                'Acceleration': acceleration
            })

        # Increment the step
        step += 1

    # Close the simulation and TraCI
    traci.close()

    # Convert the data list to a pandas DataFrame
    df = pd.DataFrame(data)

    # Optionally, save the data to a CSV file using pandas
    df.to_csv('vehicle_data.csv', index=False)

if __name__=="__main__":
    sumo_binary = checkBinary('sumo-gui')
    traci.start([sumo_binary, "-c", "./assets/maps/new/octagon.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])
    run()