import numpy as np

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

def normalize(vector):
    return vector / np.linalg.norm(vector)

def intersect_sphere(ray_origin, ray_direction, sphere):
    center_to_origin = ray_origin - sphere.center
    A = np.dot(ray_direction, ray_direction)
    B = 2 * np.dot(ray_direction, center_to_origin)
    C = np.dot(center_to_origin, center_to_origin) - sphere.radius**2
    delta = B**2 - 4*A*C
    if delta < 0:
        return None
    t1 = (-B - np.sqrt(delta)) / (2 * A)
    t2 = (-B + np.sqrt(delta)) / (2 * A)
    t = min(t1, t2)
    if t < 0:
        return None
    return ray_origin + t * ray_direction

def ray_tracer(scene, camera, image_width, image_height, viewport_width, viewport_height, projection_plane):
    bitmap = np.zeros((image_height, image_width, 3))
    aspect_ratio = float(image_width) / image_height
    viewport_width *= aspect_ratio

    for y in range(image_height):
        for x in range(image_width):
            viewport_x = (x / image_width - 0.5) * viewport_width
            viewport_y = -(y / image_height - 0.5) * viewport_height

            ray_direction = normalize(np.array([viewport_x, viewport_y, -projection_plane]))
            closest_intersection = None
            closest_distance = float("inf")
            for sphere in scene:
                intersection = intersect_sphere(camera, ray_direction, sphere)
                if intersection is not None:
                    distance = np.linalg.norm(intersection - camera)
                    if distance < closest_distance:
                        closest_intersection = intersection
                        closest_distance = distance
                        closest_sphere = sphere
            if closest_intersection is not None:
                bitmap[y][x] = closest_sphere.color
    return bitmap