import os
import sys
import traci
from sumolib import checkBinary
def run():
    traci.start(sumoCmd)
    
    while True:
        print("\nOptions:")
        print("1. Change lane")
        print("2. Change speed")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            veh_id = input("Enter the vehicle ID: ")
            new_lane = input("Enter the new lane ID: ")
            traci.vehicle.changeLane(veh_id, new_lane, 1000)
        elif choice == 2:
            veh_id = input("Enter the vehicle ID: ")
            new_speed = float(input("Enter the new speed (in m/s): "))
            traci.vehicle.setSpeed(veh_id, new_speed)
        elif choice == 3:
            break
        else:
            print("Invalid choice. Please try again.")

    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    sumoBinary = checkBinary('sumo-gui')
    # sumoCmd = [sumoBinary, "-c", "./assets/maps/New/octagon.sumocfg", "--random", "true", "--output-prefix", " TIME"]
    sumoCmd = [sumoBinary, "-c", "./assets/maps/New/octagon.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"]

    run()