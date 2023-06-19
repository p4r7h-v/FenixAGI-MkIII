import numpy as np

def basic_ray_tracer(width, height):
    camera_position = np.array([0.0, 0.0, 0.0])
    look_at = np.array([0.0, 0.0, -1.0])
    up = np.array([0.0, 1.0, 0.0])
    sphere_center = np.array([0.0, 0.0, -5.0])
    sphere_radius = 1.0
    light_position = np.array([-3.0, 3.0, -2.0])

    def ray_cast(origin, direction):
        delta = origin - sphere_center
        a = np.dot(direction, direction)
        b = 2 * np.dot(direction, delta)
        c = np.dot(delta, delta) - sphere_radius * sphere_radius
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return None  # No intersection.

        t1 = (-b - np.sqrt(discriminant)) / (2 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2 * a)

        if t1 > 0:
            return origin + t1 * direction
        elif t2 > 0:
            return origin + t2 * direction
        else:
            return None  # Intersection is behind the camera.

    result = np.zeros((height, width, 3), dtype=np.uint8)
    aspect_ratio = width / height

    for y in range(height):
        for x in range(width):
            u = (x + 0.5) / width * aspect_ratio - 0.5
            v = 0.5 - (y + 0.5) / height
            ray_dir = np.array([u, v, -1.0]) - camera_position
            ray_dir /= np.linalg.norm(ray_dir)

            intersection = ray_cast(camera_position, ray_dir)
            if intersection is not None:
                normal = intersection - sphere_center
                normal /= np.linalg.norm(normal)
                light_dir = light_position - intersection
                light_dir /= np.linalg.norm(light_dir)

                color = max(np.dot(normal, light_dir), 0) * 255
                result[y, x] = [color, color, color]

    return result