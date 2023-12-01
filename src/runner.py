import os
import sys
import traci
import traci.constants as tc
def add_custom_vehicle_type():
    traci.vehicle.addVType("custom_vehicle", accel=2.0, decel=4.5, sigma=0.5, length=5.0, maxSpeed=30.0)


def run_simulation():
    sumo_cmd = ["sumo", "-c", "./assets/maps/A13NorthCircularRoundabout/A13NorthCircularRoundabout.sumocfg"]
    traci.start(sumo_cmd)

    try:
        # Your simulation logic here
        for step in range(1000):
            traci.simulationStep()

            # Add 10 vehicles after some steps
            if step == 100:
                add_custom_vehicle_type()
                for i in range(10):
                    traci.vehicle.add(str(i), "custom_vehicle", departPos=str(i*10), departSpeed="0")

        traci.close()
    except Exception as e:
        print(f"Error during simulation: {e}")
        traci.close()

if __name__ == "__main__":
    run_simulation()
