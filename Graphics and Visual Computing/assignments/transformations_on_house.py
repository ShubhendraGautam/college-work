import pygame
import math
from pygame.locals import QUIT

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (135, 206, 250)  # Sky Blue
HUT_COLOR = (139, 69, 19)  # Saddle Brown
ROOF_COLOR = (205, 133, 63)  # Peru
DOOR_COLOR = (160, 82, 45)  # Sienna

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Transformed Hut')

# Define initial points of the hut
base_points = [(150, 400), (350, 400), (350, 250), (150, 250)]
roof_points = [(100, 250), (250, 150), (400, 250)]
door_points = [(230, 400), (270, 400), (270, 330), (230, 330)]

# Fixed point for scaling and rotation (center of the base of the hut)
fixed_point = ((base_points[0][0] + base_points[1][0]) / 2, base_points[0][1])

# Scaling transformation
def scale(points, sx, sy, fx, fy):
    return [(fx + (x - fx) * sx, fy + (y - fy) * sy) for x, y in points]

# Translation transformation
def translate(points, dx, dy):
    return [(x + dx, y + dy) for x, y in points]

# Rotation transformation
def rotate(points, angle, fx, fy):
    rad = math.radians(angle)
    return [
        (
            fx + (x - fx) * math.cos(rad) - (y - fy) * math.sin(rad),
            fy + (x - fx) * math.sin(rad) + (y - fy) * math.cos(rad)
        ) 
        for x, y in points
    ]

# Reflection about y-axis
def reflect_y(points, y_axis_pos):
    return [(2*y_axis_pos - x, y) for x, y in points]

# Shearing transformation
def shear(points, shx, shy):
    return [(x + y * shx, y + x * shy) for x, y in points]

def draw_hut(points):
    screen.fill(BACKGROUND_COLOR)
    
    # Split points into base, roof, and door
    base, roof, door = points[:4], points[4:7], points[7:]
    
    # Draw base
    pygame.draw.polygon(screen, HUT_COLOR, base)
    
    # Draw roof
    pygame.draw.polygon(screen, ROOF_COLOR, roof)
    
    # Draw door
    pygame.draw.polygon(screen, DOOR_COLOR, door)

    pygame.display.flip()

# Applying transformations in sequence
points = base_points + roof_points + door_points

points_to_shear=roof_points


# Draw initial hut
draw_hut(points)

# Wait for a few seconds before applying transformations
pygame.time.wait(2000)

points = scale(points, 2, 2, *fixed_point)
draw_hut(points)
pygame.time.wait(2000)

points = scale(points, 0.5, 0.5, *fixed_point)
draw_hut(points)
pygame.time.wait(2000)

points = translate(points, 50, 50)
draw_hut(points)
pygame.time.wait(2000)

points = rotate(points, 45, *fixed_point)
draw_hut(points)
pygame.time.wait(2000)

points = reflect_y(points, SCREEN_WIDTH / 2)
draw_hut(points)
pygame.time.wait(2000)

xyz = shear(points_to_shear, 0.2, 0.2)
draw_hut(base_points+xyz+door_points)
pygame.time.wait(2000)

# Main loop to keep the window open
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()
