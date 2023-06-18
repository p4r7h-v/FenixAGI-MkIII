import random
import time

class GasParticle:
    def __init__(self, x, y, vx, vy, chamber_width, chamber_height):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.chamber_width = chamber_width
        self.chamber_height = chamber_height

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x >= self.chamber_width or self.x <= 0:
            self.vx = -self.vx
            self.x = max(0, min(self.x, self.chamber_width))
            
        if self.y >= self.chamber_height or self.y <= 0:
            self.vy = -self.vy
            self.y = max(0, min(self.y, self.chamber_height))

def simulate_gas_particle(chamber_width, chamber_height, num_steps, dt):
    particle = GasParticle(
        x=random.uniform(0, chamber_width),
        y=random.uniform(0, chamber_height),
        vx=random.uniform(-1, 1),
        vy=random.uniform(-1, 1),
        chamber_width=chamber_width,
        chamber_height=chamber_height,
    )
    for _ in range(num_steps):
        particle.update_position(dt)
        print(f"Particle position: ({particle.x:.2f}, {particle.y:.2f})")
        time.sleep(dt)

if __name__ == "__main__":
    simulate_gas_particle(10, 10, 15, 0.5)