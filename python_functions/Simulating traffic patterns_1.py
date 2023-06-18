import random

def traffic_simulation(traffic_rate, signal_states, road_length, simulation_time, time_step=1):
    # Initialize variables
    road = [0] * road_length
    cars = []
    results = []

    for t in range(simulation_time):
        # Generate new cars
        if random.uniform(0, 1) < (traffic_rate * time_step / 3600):
            road[0] = 1
            cars.append({"position": 0, "speed": 0})

        # Move cars
        for car in cars:
            # Check if the car is at a traffic signal
            if car["position"] in signal_states and signal_states[car["position"]] == "red":
                car["speed"] = 0
            else:
                # If the car is not at a traffic signal, increase speed and check for collisions
                car["speed"] += 1
                if road[car["position"] + car["speed"]] == 1:
                    car["speed"] -= 1

            # Move the car and update road state
            road[car["position"]] = 0
            car["position"] += car["speed"]
            road_w = road_length - 1  # wrapping road
            par_pos = car["position"] % road_w
            road[par_pos] = 1

        # Calculate traffic info
        avg_speed = sum([car["speed"] for car in cars]) / len(cars)
        queue_length = sum(1 for car in cars if car["speed"] == 0)
        results.append({"time": t, "num_cars": len(cars), "avg_speed": avg_speed, "queue_length": queue_length})

    return results

# Example usage
traffic_rate = 800  # cars per hour
signal_states = {25: "red", 50: "green", 75: "red"}  # traffic signals at positions 25, 50, and 75
road_length = 100  # length of the road
simulation_time = 60  # time to run the simulation in seconds

results = traffic_simulation(traffic_rate, signal_states, road_length, simulation_time)
print(results)