import traci
import os
from sumolib import checkBinary
import pandas as pd

min_distance = 20
max_distance = 50

def run():
    # run the simulation a 20 steps to load the car into scene
    for i in range(5):
        traci.simulationStep()
    step = 20
    vehicle_ids = traci.vehicle.getIDList() # get the ids of the vehicles
    
    follower = vehicle_ids[1]
    leading = vehicle_ids[0]

    # print(traci.vehicle.getLeader(leading))
    # for vehicle in vehicle_ids:
    #     if traci.vehicle.getDistance(leading) < traci.vehicle.getDistance(vehicle):
    #         leading = vehicle
    
    data = []
    while step <=2000:
        traci.simulationStep() #take the next step
        # print(f"leader : {leading}, speed : {traci.vehicle.getSpeed(leading)}")
        # print(f"follower : {follower} , speed : { traci.vehicle.getSpeed(follower)}")
        print(step)
        leader_present = traci.vehicle.getLeader(follower)
        if leader_present is not None:
            headway  = traci.vehicle.getLeader(follower)[1]
            if headway > 20:
                traci.vehicle.setAcceleration(follower,10,60)
            elif headway < 10:
                traci.vehicle.setAcceleration(follower,1,60)
        step +=1

        if leader_present : 
            data.append({
            'leader' : leading,
            'leader speed' : traci.vehicle.getSpeed(leading),
            'follower' : follower,
            'follwer speed' : traci.vehicle.getSpeed(follower),
             'headway' : traci.vehicle.getLeader(follower)[1]
        })
        else:
            data.append({
                'leader' : leading,
                'leader speed' : traci.vehicle.getSpeed(leading),
                'follower' : follower,
                'follwer speed' : traci.vehicle.getSpeed(follower),
                'headway' : "None"
            })
    df = pd.DataFrame(data)

    # Optionally, save the data to a CSV file using pandas
    df.to_csv('simple_platooning.csv', index=False)
    traci.close()




        

if __name__ == "__main__":
    sumo_binary = checkBinary('sumo')
    # Start SUMO as a subprocess and connect with TraCI
    traci.start([sumo_binary, "-c", "./assets/maps/singlelane/singlelane.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])
    run()
