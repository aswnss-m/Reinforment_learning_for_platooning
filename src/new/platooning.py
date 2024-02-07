import traci
from sumolib import checkBinary

# sumo_binary = checkBinary('sumo-gui')

#     # Start SUMO as a subprocess and connect with TraCI
# traci.start([sumo_binary, "-c", "./assets/maps/New/octagon.sumocfg",
#                 "--tripinfo-output", "tripinfo.xml"])

# # Get the simulation step
# step = 0

# vehicle_ids = traci.vehicle.getIDList()
# # Get the first vehicle ID
# leader_id = vehicle_ids[0]

# # Get the second vehicle ID
# follower_id = vehicle_ids[1]

# # Get the initial position and speed of the leader vehicle
# leader_pos = traci.vehicle.getPosition(leader_id)
# leader_speed = traci.vehicle.getSpeed(leader_id)

# # Set the initial position and speed of the follower vehicle to match the leader vehicle
# traci.vehicle.setPosition(follower_id, leader_pos)
# traci.vehicle.setSpeed(follower_id, leader_speed)

# # Simulation loop
# while step < 10000:
#     # Get the current time headway of the follower vehicle
#     time_headway = traci.vehicle.getTimeHeadway(follower_id)

#     # If the time headway is greater than the desired time headway (e.g., 2 seconds), accelerate the follower vehicle
#     if time_headway > 2.0:
#         traci.vehicle.setAcceleration(follower_id, 1.0)

#     # If the time headway is less than the desired time headway, decelerate the follower vehicle
#     elif time_headway < 2.0:
#         traci.vehicle.setAcceleration(follower_id, -1.0)

#     # Otherwise, maintain the current speed
#     else:
#         traci.vehicle.setAcceleration(follower_id, 0.0)

#     # Step the simulation
#     traci.simulationStep()
#     step += 1

# # Close the connection to the simulation
# traci.close()

def run():
    step =0
    vehicle_ids = ('car1.0', 'car1.1')
    leader_id = vehicle_ids[0]
    follower_id = vehicle_ids[1]

    while step<=10000:
        traci.simulationStep()
        time_headway = traci.vehicle.getDistance(follower_id)
        # If the time headway is greater than the desired time headway (e.g., 2 seconds), accelerate the follower vehicle
        if time_headway > 2.0:
            traci.vehicle.setAcceleration(follower_id, 1.0,30)

        # If the time headway is less than the desired time headway, decelerate the follower vehicle
        elif time_headway < 2.0:
            traci.vehicle.setAcceleration(follower_id, -1.0,30)

        # Otherwise, maintain the current speed
        else:
            traci.vehicle.setAcceleration(follower_id, 0.0,30)
        step+=1
    traci.close()

if __name__ == "__main__":
    sumo_binary = checkBinary('sumo-gui')

    # Start SUMO as a subprocess and connect with TraCI
    traci.start([sumo_binary, "-c", "./assets/maps/New/octagon.sumocfg",
                "--tripinfo-output", "tripinfo.xml"])
    run()
