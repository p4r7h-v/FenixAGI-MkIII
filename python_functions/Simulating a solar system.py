import math

def solar_system_simulation(bodies, time_step, simulation_duration):
    """
    A basic solar system simulation function.

    Parameters:
        bodies (list): A list of celestial bodies, each element is a tuple containing the mass, x position, y position, x velocity, and y velocity of the body e.g. (mass, x_pos, y_pos, x_vel, y_vel).
        time_step (float): Time step for simulation (in seconds).
        simulation_duration (float): Total duration of the simulation (in seconds).

    Returns:
        list: A list containing the updated positions and velocities of celestial bodies after the simulation.
    """
    G = 6.67430e-11  # gravitational constant in m^3 kg^-1 s^-2

    def update_positions(bodies, time_step):
        for body in bodies:
            mass, x_pos, y_pos, x_vel, y_vel = body
            x_pos += x_vel * time_step
            y_pos += y_vel * time_step
            body[1:3] = [x_pos, y_pos]

    def update_velocities(bodies, time_step):
        for i, body1 in enumerate(bodies[:-1]):
            for j, body2 in enumerate(bodies[i+1:], i+1):
                mass1, x_pos1, y_pos1, x_vel1, y_vel1 = body1
                mass2, x_pos2, y_pos2, x_vel2, y_vel2 = body2

                dx = x_pos2 - x_pos1
                dy = y_pos2 - y_pos1
                d = math.sqrt(dx*dx + dy*dy)

                f = G * mass1 * mass2 / (d * d)
                fx = f * dx / d
                fy = f * dy / d

                ax1 = fx / mass1
                ay1 = fy / mass1
                ax2 = -fx / mass2
                ay2 = -fy / mass2

                x_vel1 += ax1 * time_step
                y_vel1 += ay1 * time_step
                x_vel2 += ax2 * time_step
                y_vel2 += ay2 * time_step

                body1[3:] = [x_vel1, y_vel1]
                body2[3:] = [x_vel2, y_vel2]

    for _ in range(int(simulation_duration / time_step)):
        update_positions(bodies, time_step)
        update_velocities(bodies, time_step)

    return bodies