import random
import numpy as np

def simulate_traffic_patterns(density, avg_speed, speed_variance, road_length, simulation_duration):
    # Initialize simulation parameters
    time = 0
    total_vehicles = round(density * road_length)
    vehicle_positions = np.zeros(total_vehicles)
    vehicle_speeds = np.random.normal(avg_speed, speed_variance, total_vehicles)
    
    # Simulate traffic flow
    while time < simulation_duration:
        # Update vehicle positions based on their speeds
        for i in range(total_vehicles):
            vehicle_positions[i] += vehicle_speeds[i]

            # Check for boundary conditions (vehicle exiting the road)
            if vehicle_positions[i] > road_length:
                vehicle_positions[i] -= road_length
        
        # Check for vehicle proximity and adjust speeds accordingly
        for i in range(total_vehicles):
            # Calculate distance to the next vehicle
            next_vehicle = vehicle_positions[(i + 1) % total_vehicles]
            distance_to_next_vehicle = next_vehicle - vehicle_positions[i]
            if distance_to_next_vehicle < 0:
                distance_to_next_vehicle += road_length

            # Check for close proximity
            if 0 < distance_to_next_vehicle < 30:
                # Slow down if too close
                vehicle_speeds[i] = max(vehicle_speeds[i] - random.random(), 0)
            elif 30 <= distance_to_next_vehicle < 60:
                # Adjust speed to the average of surrounding vehicles
                prev_vehicle = vehicle_speeds[(i - 1 + total_vehicles) % total_vehicles]
                vehicle_speeds[i] = (vehicle_speeds[i] + prev_vehicle) / 2
            else:
                # Accelerate if no vehicle in near proximity
                vehicle_speeds[i] += random.random()

        yield vehicle_positions, vehicle_speeds, time

        # Increment the time
        time += 1