import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from shapely.geometry import Polygon
from shapely.geometry import box

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Create the Pygame window
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Set up the OpenGL perspective
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1, 1)
glMatrixMode(GL_MODELVIEW)

# Function to draw a hollow square
def draw_square():
    glLineWidth(3)  # Set line width for the square
    glBegin(GL_LINE_LOOP)
    glVertex2f(-50, -50)  # Bottom-left corner
    glVertex2f(-50, 50)   # Top-left corner
    glVertex2f(50, 50)    # Top-right corner
    glVertex2f(50, -50)   # Bottom-right corner
    glEnd()

# Function to draw a polygon and clip it within the square
def draw_clipped_polygon(vertices):
    square = box(-50, -50, 50, 50)  # Create a shapely square
    polygon = Polygon(vertices)     # Create a shapely polygon from user input

    # Perform the intersection to clip the polygon
    clipped_polygon = polygon.intersection(square)

    if clipped_polygon.is_empty:
        return  # Nothing to draw if the clipped polygon is empty

    # Convert the clipped polygon to OpenGL vertices and draw it
    glLineWidth(1)  # Set line width for the polygon
    glBegin(GL_LINE_LOOP)
    for point in clipped_polygon.exterior.coords:
        glVertex2f(point[0], point[1])
    glEnd()

# Main loop
running = True
polygon_vertices = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x -= width / 2  # Adjust coordinates to match square's reference frame
            y = height / 2 - y  # Flip the y-axis to match square's reference frame
            polygon_vertices.append((x, y))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Translate the square to the center of the screen
    glTranslatef(0, 0, 0)

    # Call the function to draw the hollow square
    draw_square()

    # Draw the clipped polygon based on user input
    if len(polygon_vertices) >= 3:
        draw_clipped_polygon(polygon_vertices)

    pygame.display.flip()

pygame.quit()
