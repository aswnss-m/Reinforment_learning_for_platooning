import traci

def print_menu():
    print("1. Change speed")
    print("2. Change lane")
    print("3. Run simulation for 1000 steps")
    print("4. Quit")

def change_speed():
    new_speed = float(input("Enter new speed (km/h): "))
    traci.vehicle.setSpeed("vehicle1", new_speed)
    print("Speed changed to", new_speed, "km/h")

def change_lane():
    current_lane = traci.vehicle.getLaneIndex("vehicle1")
    if current_lane == 0:
        target_lane = 1
    else:
        target_lane = 0
    traci.vehicle.changeLane("vehicle1", target_lane, 50)
    print("Lane changed to", target_lane)

def run_simulation():
    for i in range(1000):
        traci.simulationStep()

def main():
    traci.init("sumo-traffic-light.sumocfg")
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            change_speed()
        elif choice == "2":
            change_lane()
        elif choice == "3":
            run_simulation()
        elif choice == "4":
            traci.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()